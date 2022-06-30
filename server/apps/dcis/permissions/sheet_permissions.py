"""Разрешения на работу с листами."""

from devind_helpers.permissions import BasePermission

from apps.dcis.models import Document, RowDimension, Sheet
from apps.dcis.services.divisions_services import get_user_divisions
from apps.dcis.services.privilege_services import has_privilege


class ChangeSheet(BasePermission):
    """Пропускает пользователей, которые могут изменять структуру листа."""

    @staticmethod
    def has_object_permission(context, obj: Sheet):
        return any((
            context.user.has_perm('dcis.add_project') and obj.period.project.user_id == context.user.id,
            context.user.has_perm('dcis.add_period') and obj.period.user_id == context.user.id,
            context.user.has_perm('dcis.change_sheet'),
            has_privilege(context.user.id, obj.period.id, 'change_sheet'),
        ))


class ChangeValue(BasePermission):
    """Пропускает пользователей, которые могут изменять значение ячейки в документе."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        division_ids = [division['id'] for division in get_user_divisions(context.user, obj.period.project)]
        return any((
            context.user.has_perm('dcis.change_value'),
            has_privilege(context.user.id, obj.period.id, 'change_value'),
            obj.period.multiple and obj.object_id in division_ids,
            not obj.period.multiple and obj.rowdimension_set.filter(object_id__in=division_ids).count(),
        ))


class AddChildRowDimension(BasePermission):
    """Пропускает пользователей, которые могут добавлять дочерние строки к строке."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return obj.document and obj.dynamic and any((
            context.user.has_perm('dcis.add_rowdimension'),
            has_privilege(context.user.id, obj.document.period.id, 'add_rowdimension')
        ))


class DeleteRowDimension(BasePermission):
    """Пропускает пользователей, которые могут удалять строку."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return obj.rowdimension_set.count() == 0 and any((
            context.user.has_perm('dcis.delete_rowdimension'),
            has_privilege(context.user.id, obj.document.period.id, 'delete_rowdimension'),
            obj.user_id == context.user.id
        ))
