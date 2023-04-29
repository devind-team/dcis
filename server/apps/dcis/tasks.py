"""Задачи Celery."""

from apps.core.models import User
from apps.dcis.models import Cell, Period
from devind.celery import app


@app.task
def recalculate_cell_task(user_id: int, cell_id: int) -> None:
    """Задача пересчета значений в документах для ячейки."""
    from apps.dcis.services.value_services import recalculate_cells

    user = User.objects.get(id=user_id)
    cell = Cell.objects.get(id=cell_id)
    recalculate_cells(user, cell.column.sheet.period, (cell,))


@app.task
def recalculate_all_cells_task(user_id: int, period_id: int) -> None:
    """Задача пересчета значений в документах для всех ячеек периода."""
    from apps.dcis.services.value_services import recalculate_all_cells

    user = User.objects.get(id=user_id)
    period = Period.objects.get(id=period_id)
    recalculate_all_cells(user, period)
