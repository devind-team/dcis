from dataclasses import dataclass, asdict, field
from pathlib import PosixPath
from typing import Iterator, Union, Optional

from openpyxl import Workbook, load_workbook
from openpyxl.cell.cell import Cell as OpenpyxlCell
from openpyxl.styles.colors import COLOR_INDEX, WHITE
from openpyxl.utils.cell import column_index_from_string, get_column_letter
from openpyxl.worksheet.dimensions import (
    DimensionHolder,
    RowDimension as OpenpyxlRowDimension,
    ColumnDimension as OpenpyxlColumnDimension
)
from openpyxl.worksheet.merge import MergeCell, MergedCell as OpenpyxlMergedCell
from xlsx_evaluate import ModelCompiler, Evaluator

from apps.dcis.helpers.theme_to_rgb import theme_and_tint_to_rgb
from .sheet_cache_service import FormulaContainerCache
from ..models import Cell, ColumnDimension, MergedCell, Period, RowDimension, Sheet


@dataclass
class BuildStyle:
    """Описание стилей"""
    horizontal_align: str
    vertical_align: str
    size: float
    strong: bool
    italic: bool
    strike: bool
    underline: bool
    color: str
    background: str
    border_style: dict[str, str]


@dataclass
class BuildColumnDimension:
    """Построение колонки."""
    width: int
    fixed: bool
    hidden: bool
    style: BuildStyle


@dataclass
class BuildRowDimension:
    """Построение строки."""
    height: int
    style: BuildStyle


@dataclass
class BuildCell(BuildStyle):
    """Построение ячеек."""
    column_id: int
    row_id: int
    kind: str
    coordinate: Optional[str] = None
    formula: Optional[str] = None
    comment: Optional[str] = None
    default: Optional[str] = None
    border_color: dict[str, str] = None


@dataclass
class BuildMergedCell:
    """Построение объединенных ячеек."""
    min_col: int
    min_row: int
    max_col: int
    max_row: int


@dataclass
class BuildSheet:
    name: str
    columns_dimension: dict[int, BuildColumnDimension]
    rows_dimension: dict[int, BuildRowDimension]
    cells: list[BuildCell]
    merged_cells: list[BuildMergedCell]

    cache_container: FormulaContainerCache = field(init=False)

    def __post_init__(self):
        self.cache_container = FormulaContainerCache(self.name)


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
        extract_sheets: list[BuildSheet] = self.extract()
        for position, extract_sheet in enumerate(extract_sheets):
            sheet = Sheet.objects.create(
                name=extract_sheet.name,
                position=position,
                period=period
            )
            extract_sheet.cache_container.save(sheet.pk)
            # Соотношение позиции и созданных идентификаторов
            columns_mapper: dict[int, int] = {}
            rows_mapper: dict[int, int] = {}
            columns_styles: dict[int, dict] = {}
            rows_styles: dict[int, dict] = {}
            for cell in extract_sheet.cells:
                column_id: int = cell.column_id
                row_id: int = cell.row_id
                columns_styles[column_id] = {}
                rows_styles[row_id] = {}

                if column_id not in columns_mapper:
                    column_parameters = {'index': column_id}
                    if column_id in extract_sheet.columns_dimension:
                        cd: dict = asdict(extract_sheet.columns_dimension[column_id])
                        columns_styles[column_id] = cd.pop('style')
                        column_parameters = {**column_parameters, **cd}
                    column: ColumnDimension = ColumnDimension.objects.create(sheet=sheet, **column_parameters)
                    columns_mapper[column_id] = column.id

                if row_id not in rows_mapper:
                    row_parameters = {'index': row_id}
                    if row_id in extract_sheet.rows_dimension:
                        rd = asdict(extract_sheet.rows_dimension[row_id])
                        rows_styles[row_id] = rd.pop('style')
                        row_parameters = {**row_parameters, **rd}
                    row: RowDimension = RowDimension.objects.create(sheet=sheet, **row_parameters)
                    rows_mapper[row_id] = row.id

                cell.column_id = columns_mapper[column_id]
                cell.row_id = rows_mapper[row_id]
                # Объединяем стили cell <- row <- col
                Cell.objects.create(**{
                    **columns_styles[column_id],
                    **rows_styles[row_id],
                    **{k: v for k, v in asdict(cell).items() if k != 'coordinate'}
                })

            for merged_cell in extract_sheet.merged_cells:
                MergedCell.objects.create(sheet=sheet, **asdict(merged_cell))

    def extract(self) -> list[BuildSheet]:
        """Парсинг файла Excel.

        Функция создает структуру данных, которая является первоначальной обработкой.
        После выделения необходимых данных можно осуществлять транзакционную запись в базу данных.
        Структура данных может использоваться для предварительной демонстрации планируемого отчета.
        """
        sheets: list[BuildSheet] = []
        for sheet in self.work_book.worksheets:
            name: str = sheet.title
            columns_dimension: dict[int, BuildColumnDimension] = self._parse_columns_dimension(sheet.column_dimensions)
            rows_dimension: dict[int, BuildRowDimension] = self._parse_rows_dimension(sheet.row_dimensions)
            cells: list[BuildCell] = self._parse_cells(self.work_book, sheet.rows)
            merged_cells: list[BuildMergedCell] = self._parse_merged_cells(sheet.merged_cells.ranges)
            sheets.append(BuildSheet(
                name,
                columns_dimension,
                rows_dimension,
                cells,
                merged_cells
            ))
        return self.evaluate_cells(sheets)

    def _parse_columns_dimension(self, holder: DimensionHolder) -> dict[int, BuildColumnDimension]:
        """Парсинг имеющихся колонок."""
        return {
            column_index_from_string(col_letter): BuildColumnDimension(
                column.width * 7,
                False,
                column.hidden,
                self.__border_style(column)
            ) for col_letter, column in holder.items()
        }

    def _parse_rows_dimension(self, holder: DimensionHolder) -> dict[int, BuildRowDimension]:
        """Парсинг имеющихся строк."""
        return {
            row.index: BuildRowDimension(int(row.height * 1.2), self.__border_style(row))
            for index, row in holder.items()
        }

    @staticmethod
    def __border_style(dimension: Union[OpenpyxlRowDimension, OpenpyxlColumnDimension, Cell, MergedCell]) -> BuildStyle:
        """for p in ('top', 'bottom', 'left', 'right', 'diagonal', 'diagonalDown', 'diagonalUp',)"""
        return BuildStyle(
            dimension.alignment.horizontal,
            dimension.alignment.vertical,
            dimension.font.sz,
            dimension.font.b,
            dimension.font.i,
            dimension.font.strike or False,
            dimension.font.u,
            f'#{dimension.font.color.value[2:]}'
            if dimension.font.color and dimension.font.color.type == 'rgb' else '#000000',
            '#FFFFFF' if dimension.fill.patternType is None else f'#{dimension.fill.fgColor.value[2:]}',
            {
                p: getattr(dimension.border, p).style
                for p in ('top', 'bottom', 'left', 'right', 'diagonal')
            }
        )

    @staticmethod
    def __color_transform(wb, color):
        if color and color.type == 'indexed':
            if color.index == 64 or color.index == 65:
                color = None
            else:
                color.type = 'rgb'
                color.value = COLOR_INDEX[color.index]
        if color and color.type == 'theme':
            color.type = 'rgb'
            color.value = theme_and_tint_to_rgb(wb, color.theme, color.tint)
        return color

    def _parse_cells(self, wb: Workbook, rows: Iterator[tuple[Union[OpenpyxlCell, OpenpyxlMergedCell]]]) -> list[BuildCell]:
        """Парсинг ячеек.

        Переданный параметр rows представляет собой матрицу.
        Каждая строка включает в себя массив ячеек, который соотноситься с колонками.
        """
        cells: list[BuildCell] = []
        for row in rows:
            for cell in row:
                border_color: dict[str, Union[int, str]] = {
                    positional: self.__color_transform(wb, getattr(cell.border, positional).color)
                    for positional in ('top', 'bottom', 'left', 'right', 'diagonal')
                }
                fill_color = self.__color_transform(wb, cell.fill.fgColor)
                font_color = self.__color_transform(wb, cell.font.color)

                # Временная заглушка
                if (font_color and font_color.index == 1 and cell.fill.patternType is None) or \
                        (font_color and font_color.index == 1 and fill_color.value == WHITE):
                    font_color.type = 'rgb'
                    font_color.value = '00000000'
                cells.append(BuildCell(
                    column_id=cell.column,
                    row_id=cell.row,
                    kind=cell.data_type,
                    coordinate=cell.coordinate,
                    formula=cell.value if isinstance(cell.value, str) and cell.value and cell.value[0] == '=' else None,
                    comment=cell.comment,
                    default=cell.value,
                    border_color={
                        p: f'#{c.value[2:]}' if c and c.type == 'rgb' else None
                        for p, c in border_color.items()
                    },
                    **asdict(self.__border_style(cell))
                ))
        return cells

    @staticmethod
    def _parse_merged_cells(ranges: list[MergeCell]) -> list[BuildMergedCell]:
        """Парсинг объединенных ячеек."""
        return [BuildMergedCell(rng.min_col, rng.min_row, rng.max_col, rng.max_row) for rng in ranges]

    def evaluate_cells(self, sheets: list[BuildSheet]) -> list[BuildSheet]:
        """Предварительно рассчитываем значения ячеек.

        Excel не хранит кешированные значения, вместо этого он хранит формулы.
        Нам необходимо рассчитать формулы, однако значения могут быть перекрестными.
        Поэтому нам необходимо собирать единую структуру и каждый раз формировать модель.
        """

        cells_values: dict[str, str] = {}
        for sheet in sheets:
            cells_values.update({
                self.coordinate(sheet.name, cell.column_id, cell.row_id): cell.default or 0 for cell in sheet.cells
            })
        for sheet in sheets:
            evaluate_model = ModelCompiler().read_and_parse_dict(cells_values, default_sheet=sheet.name)
            evaluator = Evaluator(evaluate_model)
            for cell in sheet.cells:
                if cell.formula:
                    cell.default = str(evaluator.evaluate(self.coordinate(sheet.name, cell.column_id, cell.row_id)))
                    sheet.cache_container.add_formula(cell.coordinate, cell.formula)
        return sheets

    @staticmethod
    def coordinate(sheet: str, column: int, row: int):
        """Получаем координату."""
        return f'{sheet}!{get_column_letter(column)}{row}'
