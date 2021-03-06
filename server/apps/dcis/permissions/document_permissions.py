"""Разрешения на работу с документами периодов."""

from dataclasses import dataclass
from typing import Any

from devind_helpers.permissions import BasePermission

from apps.dcis.models import Cell, Document, Period, RowDimension
from apps.dcis.services.divisions_services import get_user_divisions
from apps.dcis.services.document_services import get_user_documents
from apps.dcis.services.privilege_services import has_privilege
from .period_permissions import ChangePeriodSheetBase, ViewPeriod


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


class ChangeDocumentSheetBase:
    """Пропускает пользователей, которые могут изменять лист документа."""

    global_permission: str = ''
    local_permission: str = ''

    def __init__(self, context: Any, document: Document):
        self._context = context
        self._document = document
        self._can_change_period_sheet: bool | None = None
        self._has_privilege: bool | None = None

    @property
    def can_change_period_sheet(self) -> bool:
        """Может ли пользователь изменять структуру листа."""
        if self._can_change_period_sheet is None:
            self._can_change_period_sheet = ChangePeriodSheetBase.has_object_permission(
                self._context,
                self._document.period
            )
        return self._can_change_period_sheet

    @property
    def has_privilege(self) -> bool:
        """Обладает ли пользователь привилегией, позволяющей выполнять действие."""
        if self._has_privilege is None:
            self._has_privilege = self._context.user.has_perm(self.global_permission) or has_privilege(
                self._context.user.id,
                self._document.period.id,
                self.local_permission
            )
        return self._has_privilege

    @property
    def has_permission(self) -> bool:
        """Получение разрешения."""
        return self.can_change_period_sheet or self.has_privilege


class ChangeValueBase(ChangeDocumentSheetBase):
    """Пропускает пользователей, которые могут изменять значение ячейки, без проверки возможности просмотра.

    Позволяет вычислять разрешение многократно для одного пользователя
    и нескольких ячеек одного документа, не делая дополнительных запросов.
    """

    global_permission = 'dcis.change_value'
    local_permission = 'change_value'

    def __init__(self, context: Any, document: Document) -> None:
        super().__init__(context, document)
        self._user_division_ids: list[int] | None = None
        self._can_change_in_multiple_mode: bool | None = None

    @property
    def user_division_ids(self) -> list[int]:
        """Идентификаторы дивизионов пользователя."""
        if self._user_division_ids is None:
            self._user_division_ids = [
                division['id'] for division in get_user_divisions(self._context.user, self._document.period.project)
            ]
        return self._user_division_ids

    @property
    def can_change_in_multiple_mode(self) -> bool:
        """Может ли пользователь изменять ячейки, если тип сбора является множественным."""
        if self._can_change_in_multiple_mode is None:
            self._can_change_in_multiple_mode = self._document.period.multiple and (
                self._document.object_id in self.user_division_ids
            )
        return self._can_change_in_multiple_mode

    def can_change_in_single_mode(self, cell: Cell) -> bool:
        """Может ли пользователь изменять ячейку, если тип сбора является единичным."""
        if self._document.period.multiple:
            return False
        return cell.row.parent_id is None or (
            cell.row.parent_id is not None and cell.row.object_id in self.user_division_ids
        )

    def has_object_permission(self, cell: Cell) -> bool:
        """Получение разрешения."""
        if not (cell.editable and cell.formula is None):
            return False
        if self.can_change_period_sheet:
            return True
        return (
            self.has_permission or
            self.can_change_in_multiple_mode or
            self.can_change_in_single_mode(cell)
        )


class ChangeValue(BasePermission):
    """Пропускает пользователей, которые могут просматривать документ и изменять в нем значение ячейки."""

    @dataclass
    class Obj:
        document: Document
        cell: Cell

    @staticmethod
    def has_object_permission(context, obj: Obj):
        return ViewDocument.has_object_permission(
            context, obj.document
        ) and ChangeValueBase(
            context, obj.document
        ).has_object_permission(obj.cell)


class AddChildRowDimensionBase(ChangeDocumentSheetBase):
    """Пропускает пользователей, которые могут добавлять дочерние строки, без проверки возможности просмотра."""

    global_permission = 'dcis.add_rowdimension'
    local_permission = 'add_rowdimension'

    def has_object_permission(self, row: RowDimension) -> bool:
        return row.dynamic and self.has_permission


class AddChildRowDimension(BasePermission):
    """Пропускает пользователей, которые могут просматривать документ и добавлять в него дочерние строки."""

    @dataclass
    class Obj:
        document: Document
        row_dimension: RowDimension

    @staticmethod
    def has_object_permission(context, obj: Obj):
        return ViewDocument.has_object_permission(
            context, obj.document
        ) and AddChildRowDimensionBase(
            context, obj.document
        ).has_object_permission(obj.row_dimension)


class ChangeChildRowDimensionHeightBase(ChangeDocumentSheetBase):
    """Пропускает пользователей, которые могут изменять высоту дочерней строки, без проверки возможности просмотра."""

    global_permission = 'dcis.change_rowdimension'
    local_permission = 'change_rowdimension'

    def has_object_permission(self, row: RowDimension) -> bool:
        return (
            row.parent_id is not None and
            row.document_id is not None and (
                self.has_permission
                or row.user_id == self._context.user.id
            )
        )


class ChangeChildRowDimensionHeight(BasePermission):
    """Пропускает пользователей, которые могут просматривать документ и изменять в нем высоту дочерних строк."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return (
            obj.parent_id is not None and
            obj.document_id is not None and ViewDocument.has_object_permission(
                context, obj.document
            ) and ChangeChildRowDimensionHeightBase(
                context, obj.document
            ).has_object_permission(obj)
        )


class DeleteChildRowDimensionBase(ChangeDocumentSheetBase):
    """Пропускает пользователей, которые могут удалять дочерние строки, без проверки возможности просмотра."""

    global_permission = 'dcis.delete_rowdimension'
    local_permission = 'delete_rowdimension'

    def has_object_permission(self, row: RowDimension) -> bool:
        return (
            row.parent_id is not None and
            row.document_id is not None and (
                self.has_permission or
                row.user_id == self._context.user.id
            ) and row.rowdimension_set.count() == 0
        )


class DeleteChildRowDimension(BasePermission):
    """Пропускает пользователей, которые могут просматривать документ и удалять из него дочерние строки."""

    @staticmethod
    def has_object_permission(context, obj: RowDimension):
        return (
            obj.parent_id is not None and
            obj.document_id is not None and ViewDocument.has_object_permission(
                context, obj.document
            ) and DeleteChildRowDimensionBase(
                context, obj.document
            ).has_object_permission(obj)
        )
