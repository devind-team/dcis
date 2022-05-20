from pathlib import PosixPath
from typing import Iterator

from openpyexcel import Workbook, load_workbook
from openpyexcel.styles.colors import COLOR_INDEX, WHITE
from openpyexcel.utils.cell import column_index_from_string
from openpyexcel.worksheet.dimensions import DimensionHolder
from openpyexcel.worksheet.merge import MergeCell

from apps.dcis.helpers.theme_to_rgb import theme_and_tint_to_rgb
from ..models import Cell, ColumnDimension, MergedCell, Period, RowDimension, Sheet


class ExcelExtractor:
    """Парсинг xlsx файла в структуру данных для последовательной загрузки в базу данных."""

    def __init__(self, path: PosixPath):
        """Инициализация.

        :param path - путь к файлу Excel.
        """
        self.path = path
        self.work_book = load_workbook(path)

    def save(self, period: Period):
        """Сохранение обработанного файла в базу данных."""
        extract_sheets: list[dict] = self.extract()
        for position, extract_sheet in enumerate(extract_sheets):
            sheet = Sheet.objects.create(
                name=extract_sheet['name'],
                position=position,
                period=period
            )
            # Соотношение позиции и созданных идентификаторов
            columns_mapper: dict[int, int] = {}
            rows_mapper: dict[int, int] = {}
            columns_styles: dict[int, dict[str, str]] = {}
            rows_styles: dict[int, dict[str, str]] = {}
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

    def extract(self) -> list[dict]:
        """Парсинг файла Excel.

        Функция создает структуру данных, которая является первоначальной обработкой.
        После выделения необходимых данных можно осуществлять транзакционную запись в базу данных.
        Структура данных может использоваться для предварительной демонстрации планируемого отчета.
        """
        sheets: list[dict] = []
        for sheet in self.work_book.worksheets:
            name: str = sheet.title
            columns_dimension: dict[int, object] = self._parse_columns_dimension(sheet.column_dimensions)
            rows_dimension: dict[int, object] = self._parse_rows_dimension(sheet.row_dimensions)
            cells = self._parse_cells(self.work_book, sheet.rows)
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
    def _parse_columns_dimension(holder: DimensionHolder) -> dict:
        """Парсинг имеющихся колонок."""
        return {
            column_index_from_string(col_letter): {
                'width': column.width * 7,
                'fixed': False,
                'hidden': column.hidden,
                'style': {
                    'horizontal_align': column.alignment.horizontal,
                    'vertical_align': column.alignment.vertical,
                    'size': column.font.sz,
                    'strong': column.font.b,
                    'italic': column.font.i,
                    'strike': column.font.strike,
                    'underline': column.font.u,
                    'color': f'#{column.font.color.value[2:]}'
                    if column.font.color and column.font.color.type == 'rgb' else '#000000',
                    'background': '#FFFFFF'
                    if column.fill.patternType is None
                    else f'#{column.fill.fgColor.value[2:]}',
                    'border_style': {
                        'top': column.border.top.style,
                        'bottom': column.border.bottom.style,
                        'left': column.border.left.style,
                        'right': column.border.right.style,
                        'diagonal': column.border.diagonal.style
                    },
                }
            } for col_letter, column in holder.items()
        }

    @staticmethod
    def _parse_rows_dimension(holder: DimensionHolder) -> dict:
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
                    'color': f'#{row.font.color.value[2:]}'
                    if row.font.color and row.font.color.type == 'rgb' else '#000000',
                    'background': '#FFFFFF'
                    if row.fill.patternType is None
                    else f'#{row.fill.fgColor.value[2:]}',
                    'border_style': {
                        'top': row.border.top.style,
                        'bottom': row.border.bottom.style,
                        'left': row.border.left.style,
                        'right': row.border.right.style,
                        'diagonal': row.border.diagonal.style
                    }
                }
            } for index, row in holder.items()
        }

    @staticmethod
    def _parse_cells(wb: Workbook, rows: Iterator[tuple[Cell]]) -> list[dict]:
        """Парсинг ячеек.

        Переданный параметр rows представляет собой матрицу.
        Каждая строка включает в себя массив ячеек, который соотноситься с колонками.
        """
        rows_result: list[dict] = []
        for row in rows:
            for cell in row:
                top_color = cell.border.top.color
                bottom_color = cell.border.bottom.color
                left_color = cell.border.left.color
                right_color = cell.border.right.color
                diagonal_color = cell.border.diagonal.color
                fill_color = cell.fill.fgColor
                font_color = cell.font.color
                colors = [top_color, bottom_color, left_color, right_color, diagonal_color, fill_color, font_color]

                for color in colors:
                    if color and color.type == 'indexed':
                        if color.index == 64 or color.index == 65:
                            color = None
                        else:
                            color.type = 'rgb'
                            color.value = COLOR_INDEX[color.index]
                    if color and color.type == 'theme':
                        color.type = 'rgb'
                        color.value = theme_and_tint_to_rgb(wb, color.theme, color.tint)
                # Временная заглушка
                if (font_color and font_color.index == 1 and cell.fill.patternType is None) or \
                        (font_color and font_color.index == 1 and fill_color.value == WHITE):
                    font_color.type = 'rgb'
                    font_color.value = '00000000'

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
                    'strike': cell.font.strike or False,
                    'underline': cell.font.u,
                    'color': f'#{font_color.value[2:]}'
                    if font_color and font_color.type == 'rgb' else '#000000',
                    'background': '#FFFFFF'
                    if cell.fill.patternType is None
                    else f'#{cell.fill.fgColor.value[2:]}',
                    'border_style': {
                        'top': cell.border.top.style,
                        'bottom': cell.border.bottom.style,
                        'left': cell.border.left.style,
                        'right': cell.border.right.style,
                        'diagonal': cell.border.diagonal.style,
                        'diagonalDown': cell.border.diagonalDown,
                        'diagonalUp': cell.border.diagonalUp
                    },
                    'border_color': {
                        'top': f'#{top_color.value[2:]}'
                        if top_color and top_color.type == 'rgb' else None,
                        'bottom': f'#{bottom_color.value[2:]}'
                        if bottom_color and bottom_color.type == 'rgb' else None,
                        'left': f'#{left_color.value[2:]}'
                        if left_color and left_color.type == 'rgb' else None,
                        'right': f'#{right_color.value[2:]}'
                        if right_color and right_color.type == 'rgb' else None,
                        'diagonal': f'#{diagonal_color.value[2:]}'
                        if diagonal_color and diagonal_color.type == 'rgb' else None
                    }
                })
        return rows_result

    @staticmethod
    def _parse_merged_cells(ranges: list[MergeCell]) -> list[dict]:
        """Парсинг объединенных ячеек."""
        return [{
            'min_col': rng.min_col,
            'min_row': rng.min_row,
            'max_col': rng.max_col,
            'max_row': rng.max_row
        } for rng in ranges]