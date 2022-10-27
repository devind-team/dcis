"""Разрешения на работу с документами периодов."""

from django.core.exceptions import PermissionDenied

from apps.core.models import User
from apps.dcis.models import AddStatus, Cell, Document, Period, RowDimension, Status
from apps.dcis.services.divisions_services import get_user_divisions
from apps.dcis.services.privilege_services import has_privilege
from .period_permissions import can_change_period_sheet_base, can_view_period


def can_add_budget_classification(user: User):
    """Пропускает пользователей, которые могут добавлять КБК, без проверки возможности просмотра."""
    if user.has_perm('devind_dictionaries.add_budgetclassification'):
        return
    raise PermissionDenied('Недостаточно прав для добавления КБК.')


def can_view_document(user: User, document: Document):
    """Пропускает пользователей, которые могут просматривать документ."""
    from apps.dcis.services.document_services import get_user_documents
    try:
        can_view_period(user, document.period)
        if document not in get_user_documents(user, document.period):
            raise PermissionDenied('Недостаточно прав для просмотра документа.')
    except PermissionDenied:
        raise PermissionDenied('Недостаточно прав для просмотра документа.')


class AddDocumentBase:
    """Пропускает пользователей, которые могут добавлять документы в период, без проверки возможности просмотра."""

    def __init__(self, user: User, period: Period):
        self._user = user
        self._period = period
        self._user_division_ids: list[int] | None = None
        self._can_add_any_document: bool | None = None

    @property
    def user_division_ids(self) -> list[int]:
        """Идентификаторы дивизионов пользователя."""
        if self._user_division_ids is None:
            self._user_division_ids = [
                division['id'] for division in get_user_divisions(self._user, self._period.project)
            ]
        return self._user_division_ids

    @property
    def can_add_any_document(self) -> bool:
        """Может ли пользователь добавлять любой документ."""
        if self._can_add_any_document is None:
            self._can_add_any_document = (
                self._user.has_perm('dcis.add_document') or
                self._period.project.user_id == self._user.id and self._user.has_perm('dcis.add_project') or
                self._period.user_id == self._user.id and self._user.has_perm('dcis.add_period') or
                has_privilege(self._user.id, self._period.id, 'add_document')
            )
        return self._can_add_any_document

    def can_add_restricted_document(self, status: Status, division_id: int | str) -> bool:
        """Может ли пользователь добавлять документ с конкретным дивизионом и статусом."""
        add_status = AddStatus.objects.filter(from_status=None, to_status=status).first()
        return int(division_id) in self.user_division_ids and add_status is not None

    def has_object_permission(self, status: Status, division_id: int | str | None) -> bool:
        """Получение разрешения."""
        return self.can_add_any_document or (division_id and self.can_add_restricted_document(status, division_id))


def can_add_any_document(user: User, period: Period):
    """Пропускает пользователей, которые могут добавлять любой документ."""
    if AddDocumentBase(user, period).can_add_any_document:
        return
    raise PermissionDenied('Недостаточно прав для добавления документа в период.')


def can_add_document(user: User, period: Period, status: Status, division_id: int | str | None):
    """Пропускает пользователей, которые могут просматривать период и добавлять в него документы."""
    can_view_period(user, period)
    if AddDocumentBase(user, period).has_object_permission(status, division_id):
        return
    raise PermissionDenied('Недостаточно прав для добавления документа в период.')


def can_change_document_base(user: User, document: Document):
    """Пропускает пользователей, которые могут изменять документ в периоде, без проверки возможности просмотра."""
    if user.has_perm('dcis.change_document') or (
        document.period.project.user_id == user.id and user.has_perm('dcis.add_project')
    ) or (
        document.period.user_id == user.id and user.has_perm('dcis.add_period')
    ) or has_privilege(user.id, document.period.id, 'change_document'):
        return
    raise PermissionDenied('Недостаточно прав для изменения документа в периоде.')


def can_change_document_comment_base(user: User, document: Document):
    """Пропускает пользователей, которые могут изменять комментарий документа, без проверки возможности просмотра."""
    if document.user_id == user.id:
        return
    can_change_document_base(user, document)


def can_change_document_comment(user: User, document: Document):
    """Пропускает пользователей, которые могут просматривать документ и изменять его комментарий."""
    can_view_document(user, document)
    can_change_document_comment_base(user, document)


def can_add_document_status_base(user: User, document: Document, add_status: AddStatus | None):
    """Пропускает пользователей, которые могут добавлять статус документа, без проверки возможности просмотра."""
    from apps.dcis.services.document_services import get_user_roles
    if add_status is not None and len(set(get_user_roles(user, document)) & set(add_status.roles)) > 0:
        return
    can_change_document_base(user, document)


def can_add_document_status(user: User, document: Document, add_status: AddStatus | None):
    """Пропускает пользователей, которые могут просматривать документ и добавлять в него статус."""
    can_view_document(user, document)
    can_add_document_status_base(user, document, add_status)


def can_delete_document_status_base(user: User, document: Document):
    """Пропускает пользователей, которые могут удалять статус документа, без проверки возможности просмотра."""
    can_change_document_base(user, document)


def can_delete_document_status(user: User, document: Document):
    """Пропускает пользователей, которые могут просматривать документ и удалять из него статус."""
    can_view_document(user, document)
    can_delete_document_status_base(user, document)


class ChangeDocumentSheetBase:
    """Пропускает пользователей, которые могут изменять лист документа."""

    global_permission: str = ''
    local_permission: str = ''

    def __init__(self, user: User, document: Document):
        self._user = user
        self._document = document
        self._is_document_editable: bool | None = None
        self._can_change_period_sheet: bool | None = None
        self._has_privilege: bool | None = None
        self._user_division_ids: list[int] | None = None
        self._can_change_in_multiple_mode: bool | None = None

    @property
    def is_document_editable(self) -> bool:
        """Является ли документ редактируемым."""
        if self._is_document_editable is None:
            self._is_document_editable = self._document.is_editable
        return self._is_document_editable

    @property
    def can_change_period_sheet(self) -> bool:
        """Может ли пользователь изменять структуру листа."""
        if self._can_change_period_sheet is None:
            try:
                can_change_period_sheet_base(
                    self._user,
                    self._document.period
                )
            except PermissionDenied:
                self._can_change_period_sheet = False
            else:
                self._can_change_period_sheet = True
        return self._can_change_period_sheet

    @property
    def has_privilege(self) -> bool:
        """Обладает ли пользователь привилегией, позволяющей выполнять действие."""
        if self._has_privilege is None:
            self._has_privilege = self._user.has_perm(self.global_permission) or has_privilege(
                self._user.id,
                self._document.period.id,
                self.local_permission
            )
        return self._has_privilege

    @property
    def has_permission(self) -> bool:
        """Получение разрешения."""
        return self._document.user == self._user or self.can_change_period_sheet or self.has_privilege

    @property
    def user_division_ids(self) -> list[int]:
        """Идентификаторы дивизионов пользователя."""
        if self._user_division_ids is None:
            self._user_division_ids = [
                division['id'] for division in get_user_divisions(self._user, self._document.period.project)
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


class ChangeValueBase(ChangeDocumentSheetBase):
    """Пропускает пользователей, которые могут изменять значение ячейки, без проверки возможности просмотра.

    Позволяет вычислять разрешение многократно для одного пользователя
    и нескольких ячеек одного документа, не делая дополнительных запросов.
    """

    global_permission = 'dcis.change_value'
    local_permission = 'change_value'

    def can_change_in_single_mode(self, cell: Cell) -> bool:
        """Может ли пользователь изменять ячейку, если тип сбора является единичным."""
        if self._document.period.multiple:
            return False
        return cell.row.parent_id is None or (
            cell.row.parent_id is not None and cell.row.object_id in self.user_division_ids
        )

    def has_object_permission(self, cell: Cell) -> bool:
        """Получение разрешения."""
        if not (self.is_document_editable and cell.editable and cell.formula is None):
            return False
        if self.can_change_period_sheet:
            return True
        return (
            self.has_permission or
            self.can_change_in_multiple_mode or
            self.can_change_in_single_mode(cell)
        )


def can_change_value(user: User, document: Document, cell: Cell):
    """Пропускает пользователей, которые могут просматривать документ и изменять в нем значение ячейки."""
    can_view_document(user, document)
    if ChangeValueBase(user, document).has_object_permission(cell):
        return
    raise PermissionDenied('Недостаточно прав для изменения значения ячейки.')


class AddChildRowDimensionBase(ChangeDocumentSheetBase):
    """Пропускает пользователей, которые могут добавлять дочерние строки, без проверки возможности просмотра."""

    global_permission = 'dcis.add_rowdimension'
    local_permission = 'add_rowdimension'

    def can_change_in_single_mode(self, row: RowDimension) -> bool:
        """Может ли пользователь добавлять дочернюю строку, если тип сбора является единичным."""
        if self._document.period.multiple:
            return False
        return row.parent_id is None or (
            row.parent_id is not None and row.object_id in self.user_division_ids
        )

    def has_object_permission(self, row: RowDimension) -> bool:
        return self.is_document_editable and row.dynamic and (
            self.has_permission or self.can_change_in_multiple_mode or self.can_change_in_single_mode(row)
        )


def can_add_child_row_dimension(user: User, document: Document, row_dimension: RowDimension):
    """Пропускает пользователей, которые могут просматривать документ и добавлять в него дочерние строки."""
    can_view_document(user, document)
    if AddChildRowDimensionBase(user, document).has_object_permission(row_dimension):
        return
    raise PermissionDenied('Недостаточно прав для добавления дочерних строк.')


class ChangeChildRowDimensionHeightBase(ChangeDocumentSheetBase):
    """Пропускает пользователей, которые могут изменять высоту дочерней строки, без проверки возможности просмотра."""

    global_permission = 'dcis.change_rowdimension'
    local_permission = 'change_rowdimension'

    def has_object_permission(self, row: RowDimension) -> bool:
        return (
            self.is_document_editable and
            row.parent_id is not None and
            row.document_id is not None and (
                self.has_permission
                or row.user_id == self._user.id
            )
        )


def can_change_child_row_dimension_height(user: User, row: RowDimension):
    """Пропускает пользователей, которые могут просматривать документ и изменять в нем высоту дочерних строк."""
    if (
        row.parent_id is not None and
        row.document_id is not None and ChangeChildRowDimensionHeightBase(
            user, row.document
        ).has_object_permission(row)
    ):
        can_view_document(user, row.document)
        return
    raise PermissionDenied('Недостаточно прав для изменения высоты дочерней строки.')


class DeleteChildRowDimensionBase(ChangeDocumentSheetBase):
    """Пропускает пользователей, которые могут удалять дочерние строки, без проверки возможности просмотра."""

    global_permission = 'dcis.delete_rowdimension'
    local_permission = 'delete_rowdimension'

    def has_object_permission(self, row: RowDimension) -> bool:
        return (
            self.is_document_editable and
            row.parent_id is not None and
            row.document_id is not None and (
                self.has_permission or
                row.user_id == self._user.id
            ) and row.rowdimension_set.count() == 0
        )


def can_delete_child_row_dimension(user: User, row: RowDimension):
    """Пропускает пользователей, которые могут просматривать документ и удалять из него дочерние строки."""
    if (
        row.parent_id is not None and
        row.document_id is not None and DeleteChildRowDimensionBase(
            user, row.document
        ).has_object_permission(row)
    ):
        can_view_document(user, row.document)
        return
    raise PermissionDenied('Недостаточно прав для удаления строки.')
