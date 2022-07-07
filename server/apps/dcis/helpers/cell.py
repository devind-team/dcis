"""Вспомогательный модуль для расчета формул."""
from collections import defaultdict
from typing import Iterable

from django.db.models import QuerySet, Q
from openpyxl.utils.cell import get_column_letter, column_index_from_string
from openpyxl.utils.cell import coordinate_from_string
from apps.dcis.models import Cell, Document, Sheet, Value
from .sheet_cache import FormulaContainerCache


def get_dependency_cells(sheets: list[Sheet], value: Value) -> tuple[list[str], list[str]]:
    """Получаем связанные ячейки.

    Возвращается кортеж:
        - dependency - список зависимых ячеек, даже если там формула, она забирается как значение.
        - inversion - список связных ячеек, которые нужно пересчитать
    """
    dependency_cells: list[str] = []
    inversion_cells: list[str] = []
    cells: list[str] = [f'{value.sheet.name}!{get_column_letter(value.column.index)}{value.row.index}']
    sheet_containers: list[FormulaContainerCache] = [FormulaContainerCache.get(sheet) for sheet in sheets]

    while cells:
        cell = cells.pop()
        sheet_name, column_letter, row_index = parse_coordinate(cell)
        sheet_container: FormulaContainerCache
        for sheet_container in sheet_containers:
            coordinate: str = f'{column_letter}{row_index}' if sheet_name == sheet_container.sheet_name else cell
            inversions: list[str] = [
                normalize_coordinate(coord, sheet_container.sheet_name)
                for coord in sheet_container.inversion.get(coordinate, [])
            ]
            dependency: list[str] = [
                normalize_coordinate(coord, sheet_container.sheet_name)
                for coord in sheet_container.dependency.get(coordinate, {}).keys()
            ]
            dependency_cells.extend(dependency)
            inversion_cells.extend(inversions)
            cells.extend(inversions)
    return dependency_cells, inversion_cells


def resolve_cells(sheets: Iterable[Sheet], cells: set[str]) -> QuerySet[Cell]:
    """Получаем строки в зависимости от координат."""
    sheet_mapping: dict[str, int] = {sheet.name: sheet.pk for sheet in sheets}
    sheet_cells: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for cell in cells:
        sheet_name, column_letter, row = parse_coordinate(cell)
        sheet_cells[sheet_mapping[sheet_name]].append((column_index_from_string(column_letter), row,))
    query_filter = Q()
    for sheet_id, coordinates in sheet_cells.items():
        for column_index, row_index in coordinates:
            query_filter |= Q(
                column__sheet_id=sheet_id,
                column__index=column_index,
                row__index=row_index,
                row__parent__isnull=True
            )
    return Cell.objects.filter(query_filter).select_related('row', 'column').all()


def resolve_values(cells: Iterable[Cell], document: Document) -> QuerySet[Value]:
    """Получаем значения ячеек."""
    ...


def get_coordinate(sheet: Sheet, vc: Value | Cell) -> str:
    return f'{sheet.name}!{get_column_letter(vc.column.index)}{vc.row.index}'


def parse_coordinate(coord: str, default_sheet: str | None = None) -> tuple[str | None, str, int]:
    """Разбираем координаты."""
    coordinate = coord.split('!')
    if len(coordinate) == 1:
        column, row = coordinate_from_string(coordinate[0])
        return default_sheet, column, row
    column, row = coordinate_from_string(coordinate[1])
    return coordinate[0], column, row


def normalize_coordinate(coord: str, sheet_name: str | None = None) -> str:
    """Нормализация координаты, приведение к виду
        - A1 -> ИмяПоУмолчанию!A1
        - Лист1!B2 -> Лист1!B2
    """
    sheet_name, column, row = parse_coordinate(coord, sheet_name)
    return f'{sheet_name}!{column}{row}'
