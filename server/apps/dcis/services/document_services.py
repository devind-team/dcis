"""Модуль, отвечающий за работу с документами."""

from devind_helpers.orm_utils import get_object_or_none
from django.db import transaction
from django.db.models import Max, QuerySet

from apps.core.models import User
from apps.dcis.models import Cell, Document, DocumentStatus, Limitation, Period, RowDimension, Sheet, Status, Value
from apps.dcis.permissions import (
    can_add_document,
    can_add_document_status, can_change_document, can_change_document_comment,
)
from apps.dcis.services.divisions_services import get_user_divisions
from apps.dcis.services.privilege_services import has_privilege


def get_user_documents(user: User, period: Period | int | str) -> QuerySet[Document]:
    """Получение документов пользователя для периода.

    Пользователь видит период документ:
      - пользователь обладает глобальной привилегией dcis.view_document
      - пользователь создал проект документа
      - пользователь создал период документа
      - пользователь создал документ
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
    division_ids = [division['id'] for division in get_user_divisions(user, period.project)]
    if period.multiple:
        divisions_documents = Document.objects.filter(period=period, object_id__in=division_ids)
    else:
        divisions_documents = Document.objects.filter(period=period, rowdimension__object_id__in=division_ids)
    return (Document.objects.filter(period=period, user=user) | divisions_documents).distinct()


@transaction.atomic
def create_document(
    user: User,
    period: Period,
    status: Status,
    comment: str,
    document_id: int | str | None = None,
    division_id: int | str | None = None
) -> Document:
    """Добавление нового документа.

    :param user: пользователь, который создает документ
    :param period: собираемый период
    :param status: начальный статус документа
    :param comment: комментарий к документу
    :param document_id: идентификатор документа, от которого создавать копию
    :param division_id: идентификатор дивизиона
    """
    from devind_dictionaries.models import Department, Organization

    can_add_document(user, period, status, division_id)
    source_document: Document | None = get_object_or_none(Document, pk=document_id)
    try:
        object_name: str = period.project.division.objects.get(pk=division_id).name
    except (Department.DoesNotExist, Organization.DoesNotExist):
        object_name = ''
    document = Document.objects.create(
        version=(get_documents_max_version(period.id, division_id) or 0) + 1,
        comment=comment,
        object_id=division_id,
        object_name=object_name,
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
    return document


def _transfer_cells(rows_transform: dict[int, int]) -> None:
    """Перенос ячеек дочерних строк."""
    for cell in Cell.objects.filter(row_id__in=rows_transform.keys()):
        cell_id = cell.id
        cell.pk, cell.row_id = None, rows_transform[cell.row_id]
        cell.save()
        _transfer_limitations(cell_id, cell.id)


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


def _transfer_limitations(
    cell_original: int,
    cell: int,
    parent_id_original: int | None = None,
    parent_id: int | None = None
) -> None:
    """Рекурсивно переносим ограничения ячеек.

    :param cell_original: оригинальная ячейка
    :param cell: ячейка в которую переносим ограничения
    :param parent_id_original: идентификатор оригинального переносимого ограничения
    :param parent_id: идентификатор переносимого ограничения
    """
    for limitation in Limitation.objects.filter(cell_id=cell_original, parent_id=parent_id_original):
        limitation_parent = limitation.pk
        limitation.pk, limitation.cell_id, limitation.parent_id = None, cell, parent_id
        limitation.save()
        _transfer_limitations(cell_original, cell, limitation_parent, limitation.id)


def add_document_status(user: User, document: Document, status: Status, comment: str, ) -> DocumentStatus:
    """Добавление статуса документа."""
    can_add_document_status(user, document, status)
    return DocumentStatus.objects.create(
        user=user,
        document=document,
        status=status,
        comment=comment,
    )


def change_document_comment(user: User, document: Document, comment: str) -> Document:
    """Изменение комментария версии документа."""
    can_change_document_comment(user, document)
    document.comment = comment
    document.save(update_fields=('comment', 'updated_at'))
    return document


def delete_document_status(user: User, status: DocumentStatus) -> None:
    """Удаление статуса документа."""
    can_change_document(user, status.document)
    status.delete()


def get_documents_max_version(period_id: int | str, division_id: int | str | None) -> int | None:
    """Получение максимальной версии документа для периода."""
    return Document.objects.filter(
        period_id=period_id,
        object_id=division_id
    ).aggregate(version=Max('version'))['version']
