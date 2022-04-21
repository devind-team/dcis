"""Модуль работы с документами."""

from typing import Optional, Union, Type

from django.db.models import Max
from devind_helpers.orm_utils import get_object_or_404, get_object_or_none
from apps.core.models import User
from apps.dcis.models import Period, Document, Cell, Limitation, Value, Sheet, Status, RowDimension


def create_new_document(
        user: User,
        period: Period,
        document_id: int,
        status_id: int,
        comment: str,
        object_id: Optional[int] = None
) -> Document:
    """Создание нового документа.

        user - пользователь, который создает документ
        period_id - собираемый период
        status_id - идентификатор статуса устанавливаемого документа
        object_id - идентификатор дивизиона
    """
    status: Status = get_object_or_404(Status, pk=status_id)
    latest_document: Optional[Document] = get_object_or_none(Document, pk=document_id)
    max_version: Optional[int] = Document.objects.filter(
        period=period,
        object_id=object_id
    ).aggregate(version=Max('version'))['version']

    document: Document = Document.objects.create(
        version=max_version + 1 if max_version is not None else 1,
        comment=comment,
        object_id=object_id,
        period=period
    )
    document.documentstatus_set.create(
        comment='Документ создан',
        user=user,
        status=status
    )
    sheet: Sheet
    for sheet in period.sheet_set.all():
        document.sheets.add(sheet)
        if latest_document is not None:
            rows_transform: dict[Union[int, Type[int]], int] = {}
            parent_rows: list[int] = sheet.rowdimension_set \
                .filter(document=latest_document, parent__isnull=True) \
                .values_list('id', flat=True)
            for parent_row in parent_rows:
                rows_transform.update(transfer_rows(user, sheet, document, parent_row))

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


def transfer_rows(user: User, sheet: Sheet, document: Document, parent_id: int, parent_ids=None) -> dict[int, int]:
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
    rows: list[RowDimension] = document.rowdimension_set.filter(parent_id=parent_id).all()
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
        rows_transform.update(transfer_rows(user, sheet, document, row.id, rows_transform))
    return rows_transform


def transfer_limitations(
        cell_original: int,
        cell: int,
        parent_id_original: Optional[int] = None,
        parent_id: Optional[int] = None
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

