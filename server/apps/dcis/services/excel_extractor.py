from pathlib import PosixPath
from typing import List, Iterator, Tuple, Dict

from openpyexcel import load_workbook
from openpyexcel.styles.colors import COLOR_INDEX
from openpyexcel.utils.cell import column_index_from_string
from openpyexcel.worksheet.dimensions import DimensionHolder
from openpyexcel.worksheet.merge import MergeCell

from ..models import Period, Sheet, Cell, MergedCell, RowDimension, ColumnDimension


class ExcelExtractor:
    """Парсинг xlsx файла в структуру данных для последовательной загрузки в базу данных."""

    def __init__(self, path: PosixPath):
        """Инициализация.

        :param path - путь к файлу excel.
        """
        self.path = path
        self.work_book = load_workbook(path)

    def save(self, period: Period):
        """Сохранение обработанного файла в базу данных."""
        extract_sheets: List[Dict] = self.extract()
        for position, extract_sheet in enumerate(extract_sheets):
            sheet = Sheet.objects.create(
                name=extract_sheet['name'],
                position=position,
                period=period
            )
            # Соотношение позиции и созданных идентификаторов
            columns_mapper: Dict[int, int] = {}
            rows_mapper: Dict[int, int] = {}
            columns_styles: Dict[int, Dict[str, str]] = {}
            rows_styles: Dict[int, Dict[str, str]] = {}
            for cell in extract_sheet['cells']:
                column_id: int = cell['column_id']
                row_id: int = cell['row_id']
                columns_styles[column_id] = {}
                rows_styles[row_id] = {}

                if column_id not in columns_mapper:
                    column_parameters = {'index': column_id}
                    if column_id in extract_sheet['columns_dimension']:
                        columns_styles[column_id] = extract_sheet['columns_dimension'][column_id].pop('style')
                        column_parameters = {**column_parameters, **extract_sheet['columns_dimension'][column_id]}
                    column: ColumnDimension = ColumnDimension.objects.create(sheet=sheet, **column_parameters)
                    columns_mapper[column_id] = column.id

                if row_id not in rows_mapper:
                    row_parameters = {'index': row_id}
                    if row_id in extract_sheet['rows_dimension']:
                        rows_styles[row_id] = extract_sheet['rows_dimension'][row_id].pop('style')
                        row_parameters = {**row_parameters, **extract_sheet['rows_dimension'][row_id]}
                    row: RowDimension = RowDimension.objects.create(sheet=sheet, **row_parameters)
                    rows_mapper[row_id] = row.id

                cell['column_id'] = columns_mapper[column_id]
                cell['row_id'] = rows_mapper[row_id]
                # Объединяем стили cell <- row <- col
                Cell.objects.create(**{
                    **columns_styles[column_id],
                    **rows_styles[row_id],
                    **cell
                })

            for merged_cell in extract_sheet['merged_cells']:
                MergedCell.objects.create(sheet=sheet, **merged_cell)

    def extract(self) -> List[Dict]:
        """Парсинг файла эксель.

        Функция создает структуру данных, которая является первоначальной обработкой.
        После выделения необходимых данных можно осуществлять транзакционную запись в базу данных.
        Структура данных может использоваться для предварительной демонстрации планируемого отчета.
        """
        sheets: List[Dict] = []
        for sheet in self.work_book.worksheets:
            name: str = sheet.title
            columns_dimension: Dict[int, object] = self._parse_columns_dimension(sheet.column_dimensions)
            rows_dimension: Dict[int, object] = self._parse_rows_dimension(sheet.row_dimensions)
            cells = self._parse_cells(sheet.rows)
            merged_cells = self._parse_merged_cells(sheet.merged_cells.ranges)

            sheets.append({
                'name': name,
                'columns_dimension': columns_dimension,
                'rows_dimension': rows_dimension,
                'cells': cells,
                'merged_cells': merged_cells
            })
        return sheets

    @staticmethod
    def _parse_columns_dimension(holder: DimensionHolder) -> Dict:
        """Парсинг имеющихся колонок."""
        return {
            column_index_from_string(col_letter): {
                'width': column.width,
                'fixed': False,
                'hidden': column.hidden,
                'auto_size': column.auto_size,
                'style': {
                    'horizontal_align': column.alignment.horizontal,
                    'vertical_align': column.alignment.vertical,
                    'size': column.font.sz,
                    'strong': column.font.b,
                    'italic': column.font.i,
                    'strike': column.font.strike,
                    'underline': column.font.u,
                    'color': column.font.color.value
                    if column.font.color.type == 'rgb'
                    else COLOR_INDEX[column.font.color.index],
                    'background': column.fill.bgColor.value
                    if column.fill.bgColor.type == 'rgb'
                    else COLOR_INDEX[column.fill.bgColor.value]
                }
            } for col_letter, column in holder.items()
        }

    @staticmethod
    def _parse_rows_dimension(holder: DimensionHolder) -> Dict:
        """Парсинг имеющихся строк."""
        return {
            row.index: {
                'height': row.height,
                'style': {
                    'horizontal_align': row.alignment.horizontal,
                    'vertical_align': row.alignment.vertical,
                    'size': row.font.sz,
                    'strong': row.font.b,
                    'italic': row.font.i,
                    'strike': row.font.strike,
                    'underline': row.font.u,
                    'color': row.font.color.value
                    if row.font.color.type == 'rgb'
                    else COLOR_INDEX[row.font.color.index],
                    'background': row.fill.bgColor.value
                    if row.fill.bgColor.type == 'rgb'
                    else COLOR_INDEX[row.fill.bgColor.value]
                }
            } for index, row in holder.items()
        }

    @staticmethod
    def _parse_cells(rows: Iterator[Tuple[Cell]]) -> List[Dict]:
        """Парсинг ячеек.

        Переданный параметр rows представляет собой матрицу.
        Каждая строка включает в себя массив ячеек, который соотноситься с колонками.
        """
        rows_result: List[Dict] = []
        for row in rows:
            for cell in row:
                rows_result.append({
                    'column_id': cell.col_idx,
                    'row_id': cell.row,

                    'kind': cell.data_type,
                    'formula': cell.value
                    if isinstance(cell.value, str) and cell.value and cell.value[0] == '='
                    else None,
                    'comment': cell.comment,
                    'default': cell.value,
                    'horizontal_align': cell.alignment.horizontal,
                    'vertical_align': cell.alignment.vertical,
                    'size': cell.font.sz,
                    'strong': cell.font.b,
                    'italic': cell.font.i,
                    'strike': cell.font.strike,
                    'underline': cell.font.u,
                    'color': cell.font.color.value
                    if cell.font.color.type == 'rgb'
                    else COLOR_INDEX[cell.font.color.index],
                    'background': cell.fill.bgColor.value
                    if cell.fill.bgColor.type == 'rgb'
                    else COLOR_INDEX[cell.fill.bgColor.value]
                })
        return rows_result

    @staticmethod
    def _parse_merged_cells(ranges: List[MergeCell]) -> List[Dict]:
        """Парсинг объединенных ячеек."""
        return [{
            'min_col': rng.min_col,
            'min_row': rng.min_row,
            'max_col': rng.max_col,
            'max_row': rng.max_row
        } for rng in ranges]
