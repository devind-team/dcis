"""Модуль, отвечающий за работу с документами."""

from typing import Type

from devind_helpers.orm_utils import get_object_or_404, get_object_or_none
from django.db.models import Max, QuerySet

from apps.core.models import User
from apps.dcis.models import Cell, Document, Limitation, Period, RowDimension, Sheet, Status, Value, DocumentStatus
from apps.dcis.services.divisions_services import get_user_divisions
from apps.dcis.services.privilege_services import has_privilege


def get_user_documents(user: User, period: Period | int | str) -> QuerySet[Document]:
    """Получение документов пользователя для периода.

    Пользователь видит период документ:
      - пользователь обладает глобальной привилегией dcis.view_document
      - пользователь создал проект документа
      - пользователь создал период документа
      - период создан с множественным типом сбора, и
        пользователь добавлен в закрепленный за документом дивизион
      - период создан с единичным типом сбора, и
        пользователь добавлен в закрепленный за одной из строк документа дивизион
      - пользователь обладает локальной привилегией view_document,
        позволяющей просматривать все документы конкретного периода
    """
    period = Period.objects.get(pk=period) if type(period) in (int, str) else period
    if any((
        user.has_perm('dcis.view_document'),
        has_privilege(user.id, period.id, 'view_document'),
        period.project.user_id == user.id,
        period.user_id == user.id
    )):
        return Document.objects.filter(period_id=period.id)
    division_ids = [division['id'] for division in get_user_divisions(user, period.project)]
    if period.multiple:
        return Document.objects.filter(object_id__in=division_ids)
    else:
        return Document.objects.filter(rowdimension__object_id__in=division_ids)


def create_new_document(
    user: User,
    period: Period,
    status_id: int | str,
    comment: str,
    document_id: int | str | None = None,
    division_id: int | str | None = None
) -> Document:
    """Добавление нового документа.

        user - пользователь, который создает документ
        period_id - собираемый период
        status_id - идентификатор статуса устанавливаемого документа
        object_id - идентификатор дивизиона
    """
    status: Status = get_object_or_404(Status, pk=status_id)
    latest_document: Document | None = get_object_or_none(Document, pk=document_id)
    max_version: int | None = Document.objects.filter(
        period=period,
        object_id=division_id
    ).aggregate(version=Max('version'))['version']

    document: Document = Document.objects.create(
        version=max_version + 1 if max_version is not None else 1,
        comment=comment,
        object_id=division_id,
        period=period
    )
    document.documentstatus_set.create(
        comment='Документ добавлен',
        user=user,
        status=status
    )
    sheet: Sheet
    for sheet in period.sheet_set.all():
        document.sheets.add(sheet)
        if latest_document is not None:
            rows_transform: dict[int | Type[int], int] = {}
            parent_rows: list[int] = sheet.rowdimension_set \
                .filter(parent__isnull=True) \
                .values_list('id', flat=True)
            for parent_row in parent_rows:
                rows_transform.update(transfer_rows(user, sheet, latest_document, document, parent_row))

            # Копируем свойства ячеек дочерних строк
            cells: list[Cell] = Cell.objects.filter(row_id__in=rows_transform.keys()).all()
            for cell in cells:
                cell_id = cell.id
                cell.pk, cell.row_id = None, rows_transform[cell.row_id]
                cell.save()
                # Переносим ограничения
                transfer_limitations(cell_id, cell.pk)

            # Копируем значения
            values: list[Value] = Value.objects.filter(sheet=sheet, document=latest_document)
            for value in values:
                value.id, value.document, value.row_id = None, document, rows_transform.get(value.row_id, value.row_id)
                value.save()
    return document


def transfer_rows(
    user: User,
    sheet: Sheet,
    last_document: Document,
    document: Document,
    parent_id: int,
    parent_ids=None
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
    rows: list[RowDimension] = last_document.rowdimension_set.filter(parent_id=parent_id).all()
    row: RowDimension
    for row in rows:
        document_row: RowDimension = RowDimension.objects.create(
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
        rows_transform.update(transfer_rows(user, sheet, last_document, document, row.id, rows_transform))
    return rows_transform


def transfer_limitations(
    cell_original: int,
    cell: int,
    parent_id_original: int | None = None,
    parent_id: int | None = None
) -> None:
    """Рекурсивно переносим ограничения ячеек.

        cell_original - оригинальная ячейка
        cell - ячейка в которую переносим ограничения
        parent_id_original - идентификатор оригинального переносимого ограничения
        parent_id - идентификатор переносимого ограничения
    """
    limitations: list[Limitation] = Limitation.objects \
        .filter(cell_id=cell_original, parent_id=parent_id_original) \
        .all()
    for limitation in limitations:
        limitation_parent = limitation.pk
        limitation.pk, limitation.cell_id, limitation.parent_id = None, cell, parent_id
        limitation.save()
        transfer_limitations(cell_original, cell, limitation_parent, limitation.id)


def add_document_status(status: Status, document: Document, comment: str, user: User) -> DocumentStatus.status:
    """Добавление статуса документа."""
    return DocumentStatus.objects.create(
        status=status,
        document=document,
        comment=comment,
        user=user
    )
