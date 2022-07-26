"""Модуль разрешений для изменения значений"""
from django.core.exceptions import PermissionDenied
from apps.dcis.models import Cell, Document
from apps.dcis.permissions import can_change_period_sheet, can_view_document
from apps.dcis.services.divisions_services import get_user_divisions
from apps.dcis.services.privilege_services import has_privilege


def can_change_value(context, document: Document, cell: Cell):
    """Возвращает возможность изменения ячейки в документе."""
    try:
        can_view_document(context, document)
        if not (
            cell.editable and
            cell.formula is None
        ):
            raise PermissionDenied()
    except PermissionDenied:
        raise PermissionDenied('Недостаточно прав для изменения ячейки в документе')
    try:
        can_change_period_sheet(context, document.period)
    except PermissionDenied:
        division_ids = [division['id'] for division in get_user_divisions(context.user, document.period.project)]
        if not (
            context.user.has_perm('dcis.change_value') or
            has_privilege(context.user.id, document.period.id, 'change_value') or
            document.period.multiple and document.object_id in division_ids or
            not document.period.multiple and cell.row.parent_id is None or (
                not document.period.multiple and
                cell.row.parent_id is not None and
                cell.row.object_id in division_ids
            )
        ):
            raise PermissionDenied('Недостаточно прав для изменения ячейки в документе')
