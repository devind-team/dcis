"""Модуль, отвечающий за работу с агрегациями."""

import contextlib
import json

from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.schema.types import ErrorFieldType
from devind_helpers.utils import gid2int
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.files.base import File
from django.db import transaction
from django.db.models import QuerySet
from openpyxl.utils.cell import column_index_from_string, coordinate_from_string, get_column_letter
from pydantic import BaseModel, ValidationError, parse_obj_as

from apps.core.models import User
from apps.dcis.helpers.pydantic_translate import translate
from apps.dcis.models import Cell, Period, RelationshipCells, Sheet
from apps.dcis.permissions import can_change_period_sheet
from apps.dcis.permissions.period_permissions import can_change_period


CellIDType = int | str


def check_cell_permission(user: User, cell_id: CellIDType) -> Cell:
    """Проверяем привилегию на возможность изменения."""
    cell = get_object_or_404(Cell, pk=gid2int(cell_id))
    period: Period = Period.objects.get(sheet__columndimension__cell=cell)
    can_change_period_sheet(user, period)
    return cell


def add_cell_aggregation(
    user: User,
    cell_id: CellIDType,
    cells_id: list[CellIDType]
) -> tuple[list[Cell] | QuerySet[Cell], list[ErrorFieldType]]:
    """Добавляем ячейки к агрегирующей ячейке."""
    cell: Cell = check_cell_permission(user, cell_id)
    if cell.aggregation is None:
        return [], [ErrorFieldType('cell', ['Ячейка не является агрегирующей'])]
    exists_cells: list[int] = RelationshipCells.objects.filter(
        from_cell__in=cells_id,
        to_cell=cell.id
    ).values_list('from_cell', flat=True)
    cells: QuerySet[Cell] = Cell.objects \
        .filter(pk__in=cells_id, kind=cell.kind) \
        .exclude(pk__in=[cell.id, *exists_cells]).all()
    return [r.from_cell for r in [cell.to_cells.create(from_cell=c) for c in cells]], []


def delete_cell_aggregation(user: User, cell_id: CellIDType, target_cell_id: CellIDType) -> CellIDType:
    """Удаляем запись об агрегации ячеек."""
    cell: Cell = check_cell_permission(user, cell_id)
    target_cell = check_cell_permission(user, target_cell_id)
    RelationshipCells.objects.filter(to_cell=cell, from_cell=target_cell).delete()
    return target_cell_id


def calculate_aggregation_cell(cell: Cell, *raw_values) -> float:
    """Расчет агрегации для ячейки."""
    values: list[float] = []
    for raw_value in raw_values:
        with contextlib.suppress(ValueError):
            values.append(float(raw_value))

    match cell.aggregation:
        case Cell.AGGREGATION_AVG:
            return sum(values) / len(values)
        case Cell.AGGREGATION_MIN:
            return min(values)
        case Cell.AGGREGATION_MAX:
            return max(values)
        case _:
            return sum(values)


class CellsAggregation(BaseModel):
    """Возвращаемый класс запроса."""
    id: str | int
    position: str
    aggregation: str
    cells: list[str]


def get_cells_aggregation(user: User, period: Period) -> list[CellsAggregation]:
    """Получение агрегированных ячеек периода."""
    can_change_period(user, period)
    cells = Cell.objects.filter(
        column__sheet__period_id=period.id,
        aggregation__isnull=False
    ).prefetch_related('to_cells')
    return [
        CellsAggregation(
            id=cell.id,
            position=transformation_position_cell(cell),
            aggregation=cell.aggregation,
            cells=dependent_cells(cell.to_cells.all())
        )
        for cell in cells
    ]


def transformation_position_cell(cell: Cell) -> str:
    """Преобразование ячейки к нужному отображению."""
    return f"'{cell.column.sheet.name}'!{get_column_letter(cell.column.index)}{cell.row.index}"


def dependent_cells(cells: list[Cell]) -> list[str]:
    """Получение зависимых ячеек агрегации."""
    return [transformation_position_cell(cell.from_cell) for cell in cells]


class AggregationFromFileJson(BaseModel):
    """Вспомогательный класс для загрузки агрегации через json файл."""
    to_cell: str
    aggregation: str
    from_cells: list[str] | None


@transaction.atomic()
def update_aggregations_from_file(user: User, period: Period, aggregation_file: File) -> list[CellsAggregation]:
    """Обновление агрегации из json файла."""

    for cell in get_cells_aggregation(user, period):
        delete_cells_aggregation(user, cell.id)

    try:
        data = parse_obj_as(list[AggregationFromFileJson], json.load(aggregation_file))
    except json.JSONDecodeError as e:
        raise ValueError(f'Неверный формат JSON: {e.msg}.')
    except ValidationError as error:
        e = translate.translate(error.errors(), locale="ru_RU")
        raise ValueError(f"Недопустимые данные JSON: запись {e[0]['loc'][1] + 1} {e[0]['msg']} {e[0]['loc'][2]}.")

    return [
        add_aggregation_cell(
            user=user,
            period=period,
            aggregation_cell=aggregation.to_cell,
            aggregation_method=aggregation.aggregation,
            aggregation_cells=aggregation.from_cells
        ) for aggregation in data
    ]


def get_cell_aggregation_id(data_cell: str, period_id: str | int) -> str | int:
    """Получение идентификатора ячейки."""
    try:
        data = data_cell.split('!')
        sheet_name = data[0].replace('\'', '')
        column, row = coordinate_from_string(data[1])
        column = column_index_from_string(column)
        cell = Cell.objects.select_related('column__sheet').get(
            column__sheet__name=sheet_name,
            column__sheet__period__id=period_id,
            column__index=column,
            row__index=row
        )
        return cell.id
    except (Sheet.DoesNotExist, Cell.DoesNotExist):
        raise ValueError(f'Ячейка с идентификатором {cell.id} не найдена.')


def delete_cells_aggregation(user: User, cell_id: str | int) -> None:
    """Удаление агрегации и зависимых ячеек."""
    RelationshipCells.objects.filter(to_cell=cell_id).delete()
    cell = Cell.objects.get(id=cell_id)
    cell.aggregation = None
    cell.save(update_fields=('aggregation',))


@transaction.atomic
def add_aggregation_cell(
    user: User,
    period: Period,
    aggregation_cell: str,
    aggregation_method: str,
    aggregation_cells: list[str]
) -> CellsAggregation:

    to_cell_id = get_cell_aggregation_id(aggregation_cell, period.id)
    from_cell_ids = [get_cell_aggregation_id(cell, period.id) for cell in aggregation_cells]

    try:
        cell = Cell.objects.get(id=to_cell_id)
        cell.aggregation = aggregation_method
        cell.save(update_fields=('aggregation',))
    except Cell.DoesNotExist:
        raise ValueError(f'Ячейка с идентификатором {to_cell_id} не найдена.')
    except Exception as e:
        raise ValueError(f'Не удалось обновить агрегацию ячейки: {e}')

    try:
        add_cell_aggregation(user, to_cell_id, from_cell_ids)
        return CellsAggregation(
            id=to_cell_id,
            position=aggregation_cell,
            aggregation=aggregation_method,
            cells=dependent_cells(cell.to_cells.all())
        )
    except DjangoValidationError as e:
        raise ValueError(f'Не удалось добавить агрегацию ячейки: {e}')
