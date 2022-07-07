"""Модуль разрешений для изменения значений"""

from apps.dcis.models import Document, Cell
from apps.dcis.permissions import ViewDocument, ChangePeriodSheet
from apps.dcis.services.divisions_services import get_user_divisions
from apps.dcis.services.privilege_services import has_privilege


def can_change_value(context, document: Document, cell: Cell) -> bool:
    """Возвращает возможность изменения ячейки в документе."""
    if not (
        ViewDocument.has_object_permission(context, document) and
        cell.editable and
        cell.formula is None
    ):
        return False
    if ChangePeriodSheet.has_object_permission(context, document.period):
        return True
    division_ids = [division['id'] for division in get_user_divisions(context.user, document.period.project)]
    return (
        context.user.has_perm('dcis.change_value') or
        has_privilege(context.user.id, document.period.id, 'change_value') or
        document.period.multiple and document.object_id in division_ids or
        not document.period.multiple and cell.row.parent_id is None or (
            not document.period.multiple and
            cell.row.parent_id is not None and
            cell.row.object_id in division_ids
        )
    )
