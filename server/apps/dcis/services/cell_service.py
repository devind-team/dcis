"""Модуль, отвечающий за работу с метаданными ячейки."""

from django.db.models import QuerySet, Q, ExpressionWrapper
from devind_helpers.schema.types import ErrorFieldType
from devind_helpers.utils import gid2int
from devind_helpers.orm_utils import get_object_or_404
from apps.core.models import User
from apps.dcis.permissions import can_change_period_sheet
from apps.dcis.models import Cell, Period, RelationshipCells

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
