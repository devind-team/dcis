"""Модуль содержит мутации, относящиеся к значениям ячеек."""

from typing import Any

import graphene
from devind_core.schema import FileType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.schema.types import ErrorFieldType
from devind_helpers.utils import gid2int
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo

from apps.dcis.models import Cell, Document, Period, Value
from apps.dcis.permissions import can_change_period_sheet, can_change_value
from apps.dcis.schema.types import ValueInputType, ValueType
from apps.dcis.services.value_services import (
    ValueInput,
    create_file_value_archive,
    get_file_value_files,
    update_or_create_file_value,
    update_or_create_values,
)
from apps.dcis.tasks import recalculate_all_cells_task


class ChangeValuesMutation(BaseMutation):
    """Изменение значений ячеек."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')
        values = graphene.List(graphene.NonNull(ValueInputType), required=True, description='Значения ячеек')

    values = graphene.List(ValueType, description='Измененные ячейки')
    updated_at = graphene.DateTime(description='Дата изменения')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        document_id: str,
        sheet_id: str,
        values: list[ValueInputType],
    ):
        document: Document = get_object_or_404(Document, pk=gid2int(document_id))
        cells = Cell.objects.filter(id__in=[gid2int(v.cell_id) for v in values])
        errors: list[ErrorFieldType] = []
        for cell in cells:
            try:
                can_change_value(info.context.user, document, cell)
            except PermissionDenied as e:
                errors.append(ErrorFieldType('value', [str(e)]))
        if len(errors):
            return ChangeValuesMutation(success=False, errors=errors)
        values_input: list[ValueInput] = []
        for value in values:
            values_input.append(ValueInput(
                cell=next(cell for cell in cells if gid2int(value.cell_id) == cell.id),
                value=value.value,
            ))
        result = update_or_create_values(
            user=info.context.user,
            document=document,
            sheet_id=sheet_id,
            value_inputs=values_input,
        )
        return ChangeValuesMutation(values=result.values, updated_at=result.updated_at)


class ChangeFileValueMutation(BaseMutation):
    """Изменение значения ячейки типа `Файл`."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')
        cell_id = graphene.ID(required=True, description='Идентификатор ячейки')
        value = graphene.String(required=True, description='Значение')
        remaining_files = graphene.List(graphene.NonNull(graphene.ID), required=True, description='Оставшиеся файлы')
        new_files = graphene.List(graphene.NonNull(Upload), required=True, description='Новые файлы')

    value = graphene.String(required=True, description='Измененное значение')
    updated_at = graphene.DateTime(required=True, description='Дата изменения')
    value_files = graphene.List(FileType, description='Измененные файлы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        document_id: str,
        sheet_id: str,
        cell_id: str,
        value: str,
        remaining_files: list[str],
        new_files: list[InMemoryUploadedFile]
    ):
        document: Document = get_object_or_404(Document, pk=gid2int(document_id))
        cell: Cell = get_object_or_404(Cell, pk=gid2int(cell_id))

        try:
            can_change_value(info.context.user, document, cell)
        except PermissionDenied as e:
            return ChangeFileValueMutation(success=False, errors=[ErrorFieldType('value', [str(e)])])
        result = update_or_create_file_value(
            user=info.context.user,
            document=document,
            cell=cell,
            sheet_id=sheet_id,
            value=value,
            remaining_files=[gid2int(file_id) for file_id in remaining_files],
            new_files=new_files
        )
        return ChangeFileValueMutation(
            value=result.value.value,
            updated_at=result.updated_at,
            value_files=get_file_value_files(result.value)
        )


class UnloadFileValueArchiveMutation(BaseMutation):
    """Выгрузка архива значения ячейки типа `Файл`."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')
        column_id = graphene.ID(required=True, description='Идентификатор колонки')
        row_id = graphene.ID(required=True, description='Идентификатор строки')
        name = graphene.String(required=True, description='Название архива')

    src = graphene.String(description='Ссылка на сгенерированный архив')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        document_id: str,
        sheet_id: str,
        column_id: str,
        row_id: str,
        name: str
    ):
        document: Document = get_object_or_404(Document, pk=gid2int(document_id))
        return UnloadFileValueArchiveMutation(
            src=create_file_value_archive(
                user=info.context.user,
                document=document,
                value=get_object_or_404(
                    Value,
                    document_id=document.id,
                    sheet_id=sheet_id,
                    column_id=column_id,
                    row_id=row_id
                ),
                name=name
            )
        )


class RecalculateAllCells(BaseMutation):
    """Пересчет значений в документах для всех ячеек периода."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: int):
        period = get_object_or_404(Period, pk=gid2int(period_id))
        can_change_period_sheet(info.context.user, period)
        recalculate_all_cells_task.delay(info.context.user.id, period.id)
        return RecalculateAllCells()


class ValueMutations(graphene.ObjectType):
    """Мутации, связанные с ячейками."""

    change_values = ChangeValuesMutation.Field(required=True, description='Изменение значения ячейки')
    change_file_value = ChangeFileValueMutation.Field(
        required=True,
        description='Изменение значения ячейки типа `Файл`',
    )
    unload_file_value_archive = UnloadFileValueArchiveMutation.Field(
        required=True,
        description='Выгрузка архива значения ячейки типа `Файл`',
    )
    recalculate_all_cells = RecalculateAllCells.Field(
        required=True,
        description='Пересчет значений в документах для всех ячеек периода',
    )
