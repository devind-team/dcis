from typing import List, Iterator, Tuple, Dict
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import PosixPath, Path
from openpyexcel import load_workbook
from openpyexcel.worksheet.dimensions import DimensionHolder, ColumnDimension, RowDimension
from openpyexcel.cell.cell import Cell
from openpyexcel.worksheet.merge import MergeCell
from openpyexcel.utils.cell import get_column_letter, column_index_from_string
from openpyexcel.styles.colors import COLOR_INDEX


class ExcelExtractor:
    """Парсинг эксель файла в структуру данных для последовательной загрузки в базу данных."""

    def __init__(self, path: PosixPath):
        """Инициализация.

        :param path - путь к файлу excel.
        """
        self.path = path
        self.work_book = load_workbook(path)

    def extract(self) -> List[Dict]:
        """Парсинг файла эксель.

        Функция создает структуру данных, которая является первоначальной обработкой.
        После выделения необходимых данных можно осуществлять транзакционную запись в базу данных.
        Структура данных может использоваться для предварительной демонстрации планируемого отчета.
        """
        sheets: List[Dict] = []
        for sheet in self.work_book.worksheets:
            name: str = sheet.title
            columns_dimension = self._parse_columns_dimension(sheet.column_dimensions)
            rows_dimension = self._parse_rows_dimension(sheet.row_dimensions)
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
    def _parse_columns_dimension(holder: DimensionHolder) -> List[Dict]:
        """Парсинг имеющихся колонок"""
        columns: List[Dict] = []
        for col_letter, column in holder.items():
            if col_letter == 'worksheet':
                continue
            columns.append({
                'index': column_index_from_string(col_letter),
                'width': column.width,
                'fixed': False,
                'hidden': column.hidden,
                'auto_size': column.auto_size,

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
            })
        return columns

    @staticmethod
    def _parse_rows_dimension(holder: DimensionHolder) -> List[Dict]:
        """Парсинг имеющихся строк."""
        rows: List[Dict] = []
        for index, row in holder.items():
            rows.append({
                'index': row.index,
                'height': row.height,

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
            })
        return rows

    @staticmethod
    def _parse_cells(rows: Iterator[Tuple[Cell]]) -> List[Dict]:
        """Парсинг ячеек.

        Переданный параметр rows представляет собой матрицу.
        Каждая строка включает в себя массив ячеек, который соотноситься с колонками.
        """
        rows: List[Dict] = []
        for row in rows:
            for cell in row:
                rows.append({
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
        return rows

    @staticmethod
    def _parse_merged_cells(ranges: List[MergeCell]) -> List[Dict]:
        """Парсинг объединенных ячеек."""
        return [{
            'min_col': rng.min_col,
            'min_row': rng.min_row,
            'max_col': rng.max_col,
            'max_row': rng.max_row
        } for rng in ranges]
