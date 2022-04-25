from typing import Optional

import graphene
from devind_core.schema.types import FileType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Max
from django.utils.timezone import make_aware
from graphene_django_cud.mutations import DjangoUpdateMutation
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.models import User
from apps.dcis.models import Period, Document, Value, Sheet, Status, Document, DocumentStatus, RowDimension
from apps.dcis.permissions import AddDocument, AddDocumentStatus, DeleteDocumentStatus
from apps.dcis.schema.types import DocumentStatusType, DocumentType, ValueType
from apps.dcis.services.document_unload import DocumentUnload
from apps.dcis.services.value import (
    create_file_value_archive,
    get_file_value_files,
    update_or_create_file_value,
    update_or_create_value,
)
from apps.dcis.services.document_services import create_new_document


class AddDocumentMutation(BaseMutation):
    """Добавление документа."""

    class Input:
        """Входные параметры мутации.

            comment - комментарий к документу
            period_id - идентификатор периода
            status_id - идентификатор устанавливаемого статуса
            division_id - идентификатор дивизиона
            document_id - документ от которого создавать копию
        """
        comment = graphene.String(required=True, description='Комментарий')
        period_id = graphene.Int(required=True, description='Идентификатор периода')
        status_id = graphene.Int(required=True, description='Начальный статус документа')
        document_id = graphene.ID(description='Идентификатор документа')
        division_id = graphene.Int(description='Идентификатор дивизиона')

    document = graphene.Field(DocumentType, description='Созданный документ')

    @staticmethod
    @permission_classes((IsAuthenticated, AddDocument,))
    def mutate_and_get_payload(
            root: None,
            info: ResolveInfo,
            comment: str,
            period_id: str,
            status_id: int,
            document_id: Optional[int] = None,
            division_id: Optional[int] = None
    ) -> 'AddDocumentMutation':
        """Мутация для создания документа."""
        user: User = info.context.user
        period: Period = get_object_or_404(Period, pk=period_id)
        document_id: Optional[int] = from_global_id(document_id)[1] if document_id else None
        document: Document = create_new_document(
            user,
            period,
            status_id,
            comment,
            document_id,
            division_id
        )
        return AddDocumentMutation(document=document)


class ChangeDocumentCommentMutationPayload(DjangoUpdateMutation):
    """Изменение комментария версии документа."""

    class Meta:
        model = Document
        login_required = True
        only_fields = ('comment',)
        permissions = ('dcis.change_period', 'dcis.change_document',)


class AddDocumentStatusMutation(BaseMutation):
    """Добавление статуса документа."""

    class Input:
        document_id = graphene.ID(required=True, description='Документ')
        status_id = graphene.Int(required=True, description='Статус')
        comment = graphene.String(description='Комментарий')

    document_status = graphene.Field(DocumentStatusType, description='Статус документа')

    @staticmethod
    @permission_classes((IsAuthenticated, AddDocumentStatus,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_id: str, status_id: int, comment: str):
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        status: Status = get_object_or_404(Status, pk=status_id)
        document_status = DocumentStatus.objects.create(
            status=status,
            document=document,
            comment=comment,
            user=info.context.user
        )
        return AddDocumentStatusMutation(document_status=document_status)


class DeleteDocumentStatusMutation(BaseMutation):
    """Удаление статуса документа."""

    class Input:
        document_status_id = graphene.ID(required=True, description='Идентификатор статуса документа')

    id = graphene.ID(required=True, description='Идентификатор статуса документа')

    @staticmethod
    @permission_classes((IsAuthenticated, DeleteDocumentStatus,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_status_id: int, *args, **kwargs):
        delete_count, _ = DocumentStatus.objects.filter(pk=document_status_id).delete()
        return DeleteDocumentStatusMutation(success=delete_count == 1, id=document_status_id)


class UnloadDocumentMutation(BaseMutation):
    """Выгрузка документа."""

    class Input:
        document_id = graphene.ID(required=True, description='Документ')
        additional = graphene.List(
            graphene.NonNull(graphene.String, required=True),
            description='Дополнительные параметры'
        )

    src = graphene.String(description='Ссылка на сгенерированный файл')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_id: str, additional: Optional[list[str]] = None):
        if not additional:
            additional = []
        document = Document.objects.get(pk=from_global_id(document_id)[1])
        document_unload: DocumentUnload = DocumentUnload(document, info.context.get_host(), additional)
        src: str = document_unload.xlsx()
        return UnloadDocumentMutation(src=src)


class UnloadFileValueArchiveMutation(BaseMutation):
    """Выгрузка архива значения ячейки типа `Файл`."""

    class Input:
        value_id = graphene.ID(required=True, description='Идентификатор значения ячейки')

    src = graphene.String(description='Ссылка на сгенерированный архив')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, value_id: str):
        return UnloadFileValueArchiveMutation(src=create_file_value_archive(get_object_or_404(Value, pk=value_id)))


class ChangeValueMutation(BaseMutation):
    """Изменение значения."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        sheet_id = graphene.Int(required=True, description='Идентификатор листа')
        column_id = graphene.Int(required=True, description='Идентификатор колонки')
        row_id = graphene.Int(required=True, description='Идентификатор строки')
        value = graphene.String(required=True, description='Значение')

    value = graphene.Field(ValueType, description='Измененное значение')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: None,
        info: ResolveInfo,
        document_id: str,
        sheet_id: int,
        column_id: int,
        row_id: int,
        value: str
    ):
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        sheet: Sheet = get_object_or_404(Sheet, pk=sheet_id)
        val, _ = update_or_create_value(
            document=document,
            sheet=sheet,
            column_id=column_id,
            row_id=row_id,
            value=value
        )
        return ChangeValueMutation(value=val)


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

    value = graphene.Field(ValueType, description='Измененное значение')
    value_files = graphene.List(FileType, description='Измененные файлы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: None,
        info: ResolveInfo,
        document_id: str,
        sheet_id: int,
        column_id: int,
        row_id: int,
        value: str,
        remaining_files: list[int],
        new_files: list[InMemoryUploadedFile]
    ):
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        sheet: Sheet = get_object_or_404(Sheet, pk=sheet_id)
        val, _ = update_or_create_file_value(
            user=info.context.user,
            document=document,
            sheet=sheet,
            column_id=column_id,
            row_id=row_id,
            value=value,
            remaining_files=[int(from_global_id(global_id)[1]) for global_id in remaining_files],
            new_files=new_files
        )
        return ChangeFileValueMutation(value=val, value_files=get_file_value_files(val))


class DocumentMutations(graphene.ObjectType):
    """Мутации, связанные с документами."""

    add_document = AddDocumentMutation.Field(required=True)
    change_document_comment = ChangeDocumentCommentMutationPayload.Field(required=True)
    add_document_status = AddDocumentStatusMutation.Field(required=True)
    delete_document_status = DeleteDocumentStatusMutation.Field(required=True)
    unload_document = UnloadDocumentMutation.Field(required=True)

    unload_file_value_archive = UnloadFileValueArchiveMutation.Field(required=True)
    change_value = ChangeValueMutation.Field(required=True)
    change_file_value = ChangeFileValueMutation.Field(required=True)
