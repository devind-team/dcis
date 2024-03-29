"""Модуль, отвечающий за работу с документами."""

from devind_helpers.orm_utils import get_object_or_none
from devind_helpers.schema.types import ErrorFieldType
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Max, Q, QuerySet

from apps.core.models import User
from apps.dcis.helpers.exceptions import is_raises
from apps.dcis.models import Cell, Document, DocumentMessage, Period, RowDimension, Sheet, Status, Value
from apps.dcis.permissions import (can_add_document, can_change_document_base, can_view_document)
from apps.dcis.services.attribute_services import create_attribute_context, rerender_values
from apps.dcis.services.curator_services import get_curator_organizations, is_document_curator
from apps.dcis.services.divisions_services import get_user_divisions, is_document_division_member
from apps.dcis.services.privilege_services import has_privilege


def get_user_documents(user: User, period: Period | int | str) -> QuerySet[Document]:
    """Получение документов пользователя для периода.

    Пользователь видит период документ:
      - пользователь обладает глобальной привилегией dcis.view_document
      - пользователь создал проект документа
      - пользователь создал период документа
      - пользователь создал документ
      - пользователь является куратором для документа
      - период создан с множественным типом сбора, и
        пользователь добавлен в закрепленный за документом дивизион
      - период создан с единичным типом сбора, и
        пользователь добавлен в закрепленный за одной из строк документа дивизион
      - пользователь обладает локальной привилегией view_document,
        позволяющей просматривать все документы конкретного периода
    """
    period = Period.objects.get(pk=period) if type(period) in (int, str) else period
    if any(
        (
            user.has_perm('dcis.view_document'),
            has_privilege(user.id, period.id, 'view_document'),
            period.project.user_id == user.id,
            period.user_id == user.id
        )
    ):
        return Document.objects.filter(period_id=period.id)
    user_documents = Document.objects.filter(user=user, period=period)
    user_division_ids = [division['id'] for division in get_user_divisions(user, period.project)]
    if period.multiple:
        divisions_documents = Document.objects.filter(object_id__in=user_division_ids, period=period)
    else:
        divisions_documents = Document.objects.filter(rowdimension__object_id__in=user_division_ids, period=period)
    documents = user_documents | divisions_documents
    if period.project.division_name == 'department':
        return documents.distinct()
    curator_organization_ids = get_curator_organizations(user).values_list('id', flat=True)
    if period.multiple:
        documents |= Document.objects.filter(object_id__in=curator_organization_ids, period=period)
    elif period.division_set.filter(object_id__in=curator_organization_ids).count() > 0:
        return Document.objects.filter(period_id=period.id)
    return documents.distinct()


def get_user_roles(user: User, document: Document) -> list[str]:
    """Получение роли пользователя для документа."""
    roles: list[str] = []
    if not is_raises(PermissionDenied, can_change_document_base, user, document):
        roles.append('admin')
    if document.user_id == user.id:
        roles.append('creator')
    if is_document_curator(user, document):
        roles.append('curator')
    if is_document_division_member(user, document):
        roles.append('division_member')
    return roles


@transaction.atomic
def create_document(
    user: User,
    period: Period,
    status: Status,
    document_id: int | str | None = None,
    division_id: int | str | None = None
) -> tuple[Document | None, list[ErrorFieldType]]:
    """Добавление нового документа.

    :param user: пользователь, который создает документ
    :param period: собираемый период
    :param status: начальный статус документа
    :param document_id: идентификатор документа, от которого создавать копию
    :param division_id: идентификатор дивизиона
    """
    from devind_dictionaries.models import Department, Organization

    can_add_document(user, period, status, division_id)
    version = (get_documents_max_version(period.id, division_id) or 0) + 1
    if version > 1 and not period.versioning:
        message: str = 'Допустима только версия 1'
        return None, [
            ErrorFieldType('organization', [message]),
            ErrorFieldType('department', [message]),
        ]
    source_document: Document | None = get_object_or_none(Document, pk=document_id)
    try:
        object_name: str = period.project.division.objects.get(pk=division_id).name
    except (Department.DoesNotExist, Organization.DoesNotExist):
        object_name = ''
    document = Document.objects.create(
        version=(get_documents_max_version(period.id, division_id) or 0) + 1,
        object_id=division_id,
        object_name=object_name,
        updated_by=user,
        user=user,
        period=period
    )
    document.documentstatus_set.create(
        comment='Документ добавлен',
        user=user,
        status_id=status.id
    )
    for sheet in period.sheet_set.all():
        document.sheets.add(sheet)
        if source_document is not None:
            rows_transform: dict[int, int] = {}
            parent_row_ids: list[int] = sheet.rowdimension_set.filter(
                parent__isnull=True
            ).values_list('id', flat=True)
            for parent_row_id in parent_row_ids:
                rows_transform.update(_transfer_rows(user, sheet, source_document, document, parent_row_id))
            _transfer_cells(rows_transform)
            _transfer_values(sheet, document, source_document, rows_transform)
    rerender_values(user, document, create_attribute_context(user, document))
    return document, []


def create_document_message(user: User, document: Document, message: str, kind: str) -> DocumentMessage:
    """Добавление комментария к документу."""
    can_view_document(user, document)
    return DocumentMessage.objects.create(comment=message, user=user, document=document, kind=kind)


def get_documents_max_version(period_id: int | str, division_id: int | str | None) -> int | None:
    """Получение максимальной версии документа для периода."""
    return Document.objects.filter(
        period_id=period_id,
        object_id=division_id
    ).aggregate(version=Max('version'))['version']


def get_document_sheets(document: Document) -> QuerySet[Sheet]:
    """Получение листов документа."""
    project = document.period.project
    division = project.division.objects.get(pk=document.object_id)
    is_child= hasattr(division, 'parent_id') and getattr(division, 'parent_id') is not None
    sheet_filter = Q(show_child=True) if is_child else Q(show_head=True)
    return document.sheets.filter(sheet_filter).all()


def _transfer_cells(rows_transform: dict[int, int]) -> None:
    """Перенос ячеек дочерних строк."""
    for cell in Cell.objects.filter(row_id__in=rows_transform.keys()):
        cell.pk, cell.row_id = None, rows_transform[cell.row_id]
        cell.save()


def _transfer_values(
    sheet: Sheet,
    document: Document,
    source_document: Document,
    rows_transform: dict[int, int]
) -> None:
    """Перенос значений."""
    for value in Value.objects.filter(sheet=sheet, document=source_document):
        value.id, value.document, value.row_id = None, document, rows_transform.get(value.row_id, value.row_id)
        value.save()


def _transfer_rows(
    user: User,
    sheet: Sheet,
    source_document: Document,
    document: Document,
    parent_id: int,
    parent_ids: dict[int, int] | None = None
) -> dict[int, int]:
    """Переносим дочерние строки.

    Рекурсивно проходимся по строкам и создаем новые с трансфером идентификаторов для значений.
        row_id = 1 parent = none        ---->   row_id = 1, parent = none   - не участвует в трансфере
            row_id = 2 parent = 1       ---->       row_id = 5, parent = 1      transform[2] = 5
            row_id = 3 parent = 1       ---->       row_id = 6, parent = 1      transform[3] = 6
                row_id = 4 parent - 3   ---->           row_id = 7, parent = transform[parent_id = 3] = 6
    """
    if parent_ids is None:
        parent_ids = {}

    rows_transform: dict[int, int] = {}
    for row in source_document.rowdimension_set.filter(parent_id=parent_id):
        document_row = RowDimension.objects.create(
            index=row.index,
            height=row.height,
            dynamic=row.dynamic,
            object_id=row.object_id,
            aggregation=row.aggregation,
            user=user,
            sheet=sheet,
            document=document,
            parent_id=parent_ids.get(parent_id, parent_id)
        )
        rows_transform[row.id] = document_row.id
        rows_transform.update(_transfer_rows(user, sheet, source_document, document, row.id, rows_transform))
    return rows_transform
