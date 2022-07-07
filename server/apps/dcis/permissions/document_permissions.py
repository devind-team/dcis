"""Разрешения на работу с документами периодов."""

from devind_helpers.permissions import BasePermission

from apps.dcis.models import Document, Period, RowDimension
from apps.dcis.services.document_services import get_user_documents
from apps.dcis.services.privilege_services import has_privilege
from .period_permissions import ViewPeriod, ChangePeriodSheet


class ViewDocument(BasePermission):
    """Пропускает пользователей, которые могут просматривать документ."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return (
            ViewPeriod.has_object_permission(context, obj.period) and
            obj in get_user_documents(context.user, obj.period)
        )


class AddDocument(BasePermission):
    """Пропускает пользователей, которые могут добавлять документы в период."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ViewPeriod.has_object_permission(context, obj) and (
            context.user.has_perm('dcis.add_document') or
            obj.project.user_id == context.user.id and context.user.has_perm('dcis.add_project') or
            obj.user_id == context.user.id and context.user.has_perm('dcis.add_period') or
            has_privilege(context.user.id, obj.id, 'add_document')
        )


class ChangeDocument(BasePermission):
    """Пропускает пользователей, которые могут изменять документ в периоде."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return ViewDocument.has_object_permission(context, obj) and (
            context.user.has_perm('dcis.change_document') or (
                obj.period.project.user_id == context.user.id and context.user.has_perm('dcis.add_project')
            ) or (
                obj.period.user_id == context.user.id and context.user.has_perm('dcis.add_period')
            ) or has_privilege(context.user.id, obj.id, 'change_document')
        )


class DeleteDocument(BasePermission):
    """Пропускает пользователей, которые могут удалять документ в периоде."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return ViewDocument.has_object_permission(context, obj) and (
            context.user.has_perm('dcis.delete_document') or (
                obj.period.project.user_id == context.user.id and context.user.has_perm('dcis.add_project')
            ) or (
                obj.period.user_id == context.user.id and context.user.has_perm('dcis.add_period')
            ) or has_privilege(context.user.id, obj.id, 'delete_document')
        )


class AddChildRowDimension(BasePermission):
    """Пропускает пользователей, которые могут добавлять дочерние строки к строке."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return (
            obj.document is not None and
            obj.dynamic and
            ViewDocument.has_object_permission(context, obj.document) and (
                ChangePeriodSheet.has_object_permission(context, obj.document.period) or
                context.user.has_perm('dcis.add_rowdimension') or
                has_privilege(context.user.id, obj.document.period.id, 'add_rowdimension')
            )
        )


class DeleteChildRowDimension(BasePermission):
    """Пропускает пользователей, которые могут удалять дочерние строки."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return (
            obj.document is not None and
            obj.rowdimension_set.count() == 0 and
            ViewDocument.has_object_permission(context, obj.document) and (
                ChangePeriodSheet.has_object_permission(context, obj.document.period) or
                context.user.has_perm('dcis.delete_rowdimension') or
                has_privilege(context.user.id, obj.document.period.id, 'delete_rowdimension') or
                obj.user_id == context.user.id
            )
        )
