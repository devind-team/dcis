"""Задачи Celery."""

from apps.core.models import User
from apps.dcis.models import Cell
from devind.celery import app


@app.task
def recalculate_cell_formula_task(user_id: int, cell_id: int) -> None:
    """Задача пересчета значений в документах для ячейки."""
    from apps.dcis.services.sheet_services import recalculate_cell_formula

    user = User.objects.get(id=user_id)
    cell = Cell.objects.get(id=cell_id)
    recalculate_cell_formula(user, cell)
