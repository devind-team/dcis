"""Разрешения на работу с документами периодов."""

from dataclasses import dataclass

from devind_helpers.permissions import BasePermission

from apps.dcis.models import Cell, Document, Period, RowDimension
from apps.dcis.services.divisions_services import get_user_divisions
from apps.dcis.services.document_services import get_user_documents
from apps.dcis.services.privilege_services import has_privilege
from .period_permissions import ChangePeriodSheet, ChangePeriodSheetBase, ViewPeriod


class ViewDocument(BasePermission):
    """Пропускает пользователей, которые могут просматривать документ."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return (
            ViewPeriod.has_object_permission(context, obj.period) and
            obj in get_user_documents(context.user, obj.period)
        )


class AddDocumentBase(BasePermission):
    """Пропускает пользователей, которые могут добавлять документы в период, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return (
            context.user.has_perm('dcis.add_document') or
            obj.project.user_id == context.user.id and context.user.has_perm('dcis.add_project') or
            obj.user_id == context.user.id and context.user.has_perm('dcis.add_period') or
            has_privilege(context.user.id, obj.id, 'add_document')
        )


class AddDocument(BasePermission):
    """Пропускает пользователей, которые могут просматривать период и добавлять в него документы."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ViewPeriod.has_object_permission(
            context, obj
        ) and AddDocumentBase.has_object_permission(
            context, obj
        )


class ChangeDocumentBase(BasePermission):
    """Пропускает пользователей, которые могут изменять документ в периоде, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return context.user.has_perm('dcis.change_document') or (
            obj.period.project.user_id == context.user.id and context.user.has_perm('dcis.add_project')
        ) or (
            obj.period.user_id == context.user.id and context.user.has_perm('dcis.add_period')
        ) or has_privilege(context.user.id, obj.id, 'change_document')


class ChangeDocument(BasePermission):
    """Пропускает пользователей, которые могут просматривать и изменять документ в периоде."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return ViewDocument.has_object_permission(
            context, obj
        ) and ChangeDocumentBase.has_object_permission(
            context, obj
        )


class DeleteDocumentBase(BasePermission):
    """Пропускает пользователей, которые могут удалять документ в периоде, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return context.user.has_perm('dcis.delete_document') or (
            obj.period.project.user_id == context.user.id and context.user.has_perm('dcis.add_project')
        ) or (
            obj.period.user_id == context.user.id and context.user.has_perm('dcis.add_period')
        ) or has_privilege(context.user.id, obj.id, 'delete_document')


class DeleteDocument(BasePermission):
    """Пропускает пользователей, которые могут просматривать и удалять документ в периоде."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return ViewDocument.has_object_permission(
            context, obj
        ) and DeleteDocumentBase.has_object_permission(
            context, obj
        )


class ChangeValueBase(BasePermission):
    """Пропускает пользователей, которые могут изменять значение ячейки, без проверки возможности просмотра."""

    @dataclass
    class Obj:
        document: Document
        cell: Cell

    @staticmethod
    def has_object_permission(context, obj: Obj):
        if not (obj.cell.editable and obj.cell.formula is None):
            return False
        if ChangePeriodSheetBase.has_object_permission(context, obj.document.period):
            return True
        division_ids = [division['id'] for division in get_user_divisions(context.user, obj.document.period.project)]
        return (
            context.user.has_perm('dcis.change_value') or
            has_privilege(context.user.id, obj.document.period.id, 'change_value') or
            obj.document.period.multiple and obj.document.object_id in division_ids or
            not obj.document.period.multiple and obj.cell.row.parent_id is None or (
                not obj.document.period.multiple and
                obj.cell.row.parent_id is not None and
                obj.cell.row.object_id in division_ids
            )
        )


class ChangeValue(BasePermission):
    """Пропускает пользователей, которые могут просматривать документ и изменять в нем значение ячейки."""

    @staticmethod
    def has_object_permission(context, obj: ChangeValueBase.Obj):
        if not (
            ViewDocument.has_object_permission(context, obj.document) and
            obj.cell.editable and
            obj.cell.formula is None
        ):
            return False
        return ChangePeriodSheet.has_object_permission(
            context, obj.document.period
        ) or ChangeValueBase.has_object_permission(
            context, obj
        )


class AddChildRowDimensionBase(BasePermission):
    """Пропускает пользователей, которые могут добавлять дочерние строки, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return (
            obj.document is not None and
            obj.dynamic and (
                ChangePeriodSheet.has_object_permission(context, obj.document.period) or
                context.user.has_perm('dcis.add_rowdimension') or
                has_privilege(context.user.id, obj.document.period.id, 'add_rowdimension')
            )
        )


class AddChildRowDimension(BasePermission):
    """Пропускает пользователей, которые могут просматривать документ и добавлять в него дочерние строки."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return obj.document is not None and ViewDocument.has_object_permission(
            context, obj.document
        ) and AddChildRowDimensionBase.has_object_permission(
            context, obj
        )


class ChangeChildRowDimensionHeightBase(BasePermission):
    """Пропускает пользователей, которые могут изменять высоту дочерней строки, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return (
            obj.document is not None and (
                ChangePeriodSheet.has_object_permission(context, obj.document.period) or
                context.user.has_perm('dcis.change_rowdimension') or
                has_privilege(context.user.id, obj.document.period.id, 'change_rowdimension') or
                obj.user_id == context.user.id
            )
        )


class ChangeChildRowDimensionHeight(BasePermission):
    """Пропускает пользователей, которые могут просматривать документ и изменять в нем высоту дочерних строк."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return obj.document is not None and ViewDocument.has_object_permission(
            context, obj.document
        ) and ChangeChildRowDimensionHeightBase.has_object_permission(
            context, obj
        )


class DeleteChildRowDimensionBase(BasePermission):
    """Пропускает пользователей, которые могут удалять дочерние строки, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return (
            obj.document is not None and
            obj.rowdimension_set.count() == 0 and (
                ChangePeriodSheet.has_object_permission(context, obj.document.period) or
                context.user.has_perm('dcis.delete_rowdimension') or
                has_privilege(context.user.id, obj.document.period.id, 'delete_rowdimension') or
                obj.user_id == context.user.id
            )
        )


class DeleteChildRowDimension(BasePermission):
    """Пропускает пользователей, которые могут просматривать документ и удалять из него дочерние строки."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return obj.document is not None and ViewDocument.has_object_permission(
            context, obj.document
        ) and DeleteChildRowDimensionBase.has_object_permission(
            context, obj
        )
