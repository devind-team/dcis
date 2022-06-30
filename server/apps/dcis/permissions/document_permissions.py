"""Разрешения на работу с документами периодов."""

from devind_helpers.permissions import BasePermission

from apps.dcis.models import Document, Period
from apps.dcis.permissions.period_permissions import ViewPeriod
from apps.dcis.services.document_services import get_user_documents
from apps.dcis.services.privilege_services import has_privilege


class ViewDocument(BasePermission):
    """Пропускает пользователей, которые могут просматривать документ."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return all((
            ViewPeriod.has_object_permission(context, obj.period),
            obj in get_user_documents(context.user, obj.period),
        ))


class AddDocument(BasePermission):
    """Пропускает пользователей, которые могут добавлять документы в период."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return all((
            ViewPeriod.has_object_permission(context, obj),
            any((
                context.user.has_perm('dcis.add_period'),
                obj.project.user_id == context.user.id and context.user.has_perm('dcis.add_project'),
                obj.user_id == context.user.id and context.user.has_perm('dcis.add_period'),
                has_privilege(context.user.id, obj.id, 'add_document')
            ))
        ))


class ChangeDocument(BasePermission):
    """Пропускает пользователей, которые могут изменять документ в периоде."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return ViewDocument.has_object_permission(context, obj) and any((
            context.user.has_perm('dcis.change_document'),
            all((
                obj.period.project.user_id == context.user.id,
                context.user.has_perm('dcis.add_project'),
            )),
            all((
                obj.period.user_id == context.user.id,
                context.user.has_perm('dcis.add_period'),
            )),
            has_privilege(context.user.id, obj.id, 'change_document')
        ))


class DeleteDocument(BasePermission):
    """Пропускает пользователей, которые могут удалять документ в периоде."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return ViewDocument.has_object_permission(context, obj) and any((
            context.user.has_perm('dcis.delete_document'),
            all((
                obj.period.project.user_id == context.user.id,
                context.user.has_perm('dcis.add_project'),
            )),
            all((
                obj.period.user_id == context.user.id,
                context.user.has_perm('dcis.add_period'),
            )),
            has_privilege(context.user.id, obj.id, 'delete_document')
        ))
