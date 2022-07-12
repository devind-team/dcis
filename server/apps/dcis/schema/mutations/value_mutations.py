"""Модуль содержит мутации, относящиеся к значениям ячеек."""

from typing import Any
import graphene
from devind_core.schema import FileType
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from graphql_relay import from_global_id

from apps.dcis.models import Value, Cell, Document
from apps.dcis.permissions import ChangeValue
from apps.dcis.schema.types import ValueType
from apps.dcis.services.value_services import update_or_create_value, update_or_create_file_value, \
    create_file_value_archive, get_file_value_files


class ChangeValueMutation(BaseMutation):
    """Изменение значения ячейки."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        cell_id = graphene.Int(required=True, description='Идентификатор ячейки')
        sheet_id = graphene.Int(required=True, description='Идентификатор листа')
        value = graphene.String(required=True, description='Значение')

    values = graphene.List(ValueType, description='Измененные ячейки')
    updated_at = graphene.DateTime(required=True, description='Дата изменения')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangeValue,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        document_id: str,
        cell_id: int,
        sheet_id: int,
        value: str
    ):
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        cell: Cell = get_object_or_404(Cell, pk=cell_id)
        info.context.check_object_permissions(info.context, (document, cell,))
        result = update_or_create_value(
            document=document,
            cell=cell,
            sheet_id=sheet_id,
            value=value
        )
        return ChangeValueMutation(values=result.values, updated_at=result.updated_at)


class ChangeFileValueMutation(BaseMutation):
    """Изменение значения ячейки типа `Файл`."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        sheet_id = graphene.Int(required=True, description='Идентификатор листа')
        column_id = graphene.Int(required=True, description='Идентификатор колонки')
        row_id = graphene.Int(required=True, description='Идентификатор строки')
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
        sheet_id: int,
        column_id: int,
        row_id: int,
        value: str,
        remaining_files: list[str],
        new_files: list[InMemoryUploadedFile]
    ):
        result = update_or_create_file_value(
            user=info.context.user,
            document_id=from_global_id(document_id)[1],
            sheet_id=sheet_id,
            column_id=column_id,
            row_id=row_id,
            value=value,
            remaining_files=[int(from_global_id(global_id)[1]) for global_id in remaining_files],
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
        sheet_id = graphene.Int(required=True, description='Идентификатор листа')
        column_id = graphene.Int(required=True, description='Идентификатор колонки')
        row_id = graphene.Int(required=True, description='Идентификатор строки')
        name = graphene.String(required=True, description='Название архива')

    src = graphene.String(description='Ссылка на сгенерированный архив')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        document_id: str,
        sheet_id: int,
        column_id: int,
        row_id: int,
        name: str
    ):
        return UnloadFileValueArchiveMutation(
            src=create_file_value_archive(
                value=get_object_or_404(
                    Value,
                    document_id=from_global_id(document_id)[1],
                    sheet_id=sheet_id,
                    column_id=column_id,
                    row_id=row_id
                ),
                name=name
            )
        )


class ValueMutations(graphene.ObjectType):
    """Мутации, связанные с ячейками."""
    change_value = ChangeValueMutation.Field(required=True, description='Изменение значения ячейки')
    change_file_value = ChangeFileValueMutation.Field(
        required=True,
        description='Изменение значения ячейки типа `Файл`'
    )
    unload_file_value_archive = UnloadFileValueArchiveMutation.Field(
        required=True,
        description='Выгрузка архива значения ячейки типа `Файл`'
    )