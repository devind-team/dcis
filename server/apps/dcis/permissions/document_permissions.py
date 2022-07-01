"""Разрешения на работу с документами периодов."""

from dataclasses import dataclass

from devind_helpers.permissions import BasePermission

from apps.dcis.models import Cell, Document, Period, RowDimension
from apps.dcis.services.divisions_services import get_user_divisions
from apps.dcis.services.document_services import get_user_documents
from apps.dcis.services.privilege_services import has_privilege
from .period_permissions import ViewPeriod, ChangePeriodSheet


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
                context.user.has_perm('dcis.add_document'),
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


class ChangeValue(BasePermission):
    """Пропускает пользователей, которые могут изменять значение ячейки в документе."""

    @dataclass
    class Obj:
        document: Document
        cell: Cell

    @staticmethod
    def has_object_permission(context, obj: Obj):
        if not all((
            ViewDocument.has_object_permission(context, obj.document),
            obj.cell.editable,
            obj.cell.formula is None
        )):
            return False
        if ChangePeriodSheet.has_object_permission(context, obj.document.period):
            return True
        division_ids = [division['id'] for division in get_user_divisions(context.user, obj.document.period.project)]
        return any((
            context.user.has_perm('dcis.change_value'),
            has_privilege(context.user.id, obj.document.period.id, 'change_value'),
            obj.document.period.multiple and obj.document.object_id in division_ids,
            all((
                not obj.document.period.multiple,
                obj.cell.row.parent_id is None,
            )),
            all((
                not obj.document.period.multiple,
                obj.cell.row.parent_id is not None,
                obj.cell.row.object_id in division_ids,
            ))
        ))


class AddChildRowDimension(BasePermission):
    """Пропускает пользователей, которые могут добавлять дочерние строки к строке."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return all((
            obj.document,
            obj.dynamic,
            ViewDocument.has_object_permission(context, obj.document),
            any((
                ChangePeriodSheet.has_object_permission(context, obj.document.period),
                context.user.has_perm('dcis.add_rowdimension'),
                has_privilege(context.user.id, obj.document.period.id, 'add_rowdimension')
            ))
        ))


class DeleteChildRowDimension(BasePermission):
    """Пропускает пользователей, которые могут удалять дочерние строки."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return all((
            obj.document,
            obj.rowdimension_set.count() == 0,
            ViewDocument.has_object_permission(context, obj.document),
            any((
                ChangePeriodSheet.has_object_permission(context, obj.document.period),
                context.user.has_perm('dcis.delete_rowdimension'),
                has_privilege(context.user.id, obj.document.period.id, 'delete_rowdimension'),
                obj.user_id == context.user.id
            ))
        ))
