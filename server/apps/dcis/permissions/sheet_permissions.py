from devind_helpers.permissions import BasePermission

from apps.dcis.models import Document, RowDimension, Sheet
from apps.dcis.services.divisions_services import document_in_user_divisions
from apps.dcis.services.privilege_services import has_privilege


class ChangeSheet(BasePermission):
    """Пропускает пользователей, которые могут менять структуру листа."""

    @staticmethod
    def has_object_permission(context, obj: Sheet):
        return any((
            context.user.has_perm('dcis.change_sheet'),
            has_privilege(context.user.id, obj.period.id, 'change_sheet'),
            context.user.has_perm('dcis.add_period') and obj.period.user_id == context.user.id,
        ))


class AddChildRowDimension(BasePermission):
    """Пропускает пользователей, которые могут добавлять дочерние строки к строке."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return obj.document and obj.dynamic and any((
            context.user.has_perm('dcis.add_rowdimension'),
            document_in_user_divisions(obj.document, context.user)
        ))


class DeleteRowDimension(BasePermission):
    """Пропускает пользователей, которые могут удалять строку."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return any((
            context.user.has_perm('dcis.delete_rowdimension'),
            obj.document and any((
                has_privilege(context.user.id, obj.document.period.id, 'delete_rowdimension'),
                obj.user_id == context.user.id and obj.rowdimension_set.count() == 0,
            )),
        ))


class ViewDocument(BasePermission):
    """Пропускает пользователей, которые могут просматривать документ."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return any((
            context.user.has_perm('dcis.view_document'),
            has_privilege(context.user.id, obj.period.id, 'view_document'),
            document_in_user_divisions(obj, context.user),
        ))
