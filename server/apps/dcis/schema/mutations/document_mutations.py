from datetime import datetime
from typing import Optional, List

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from django.utils.timezone import make_aware
from graphene_django_cud.mutations import DjangoUpdateMutation
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import Period, Document, Value, Sheet, Status, DocumentStatus, RowDimension
from apps.dcis.permissions import AddDocument, AddDocumentStatus, DeleteDocumentStatus
from apps.dcis.schema.types import DocumentType, ValueType, DocumentStatusType
from apps.dcis.services.document_unload import DocumentUnload
from apps.dcis.services.document_services import create_new_document


class AddDocumentMutation(BaseMutation):
    """Добавление документа."""

    class Input:
        comment = graphene.String(required=True, description='Комментарий')
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        status_id = graphene.Int(required=True, description='Начальный статус документа')
        document_id = graphene.ID(description='Идентификатор документа')

    document = graphene.Field(DocumentType, description='Созданный документ')

    @staticmethod
    @permission_classes((IsAuthenticated, AddDocument,))
    def mutate_and_get_payload(
            root: None,
            info: ResolveInfo,
            comment: str,
            period_id: str,
            status_id: int,
            document_id: Optional[str]
    ) -> 'AddDocumentMutation':
        """Мутация для создания документа."""
        period: Period = get_object_or_404(Period, pk=from_global_id(period_id)[1])
        # divisions = period.project.division.objects.filter(Q(user=u) | Q(users=u)).all()
        document_id = from_global_id(document_id)[1]
        # Служба поддержки
        object_id: int = 1

        document = create_new_document(
            info.context.user,
            period,
            document_id,
            status_id,
            comment,
            object_id
        )
        return AddDocumentMutation(document=document)


class ChangeDocumentCommentMutationPayload(DjangoUpdateMutation):
    """Изменение комментария версии документа"""

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
        """Мутация удаления статуса документа"""
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
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_id: str, additional: Optional[List[str]] = None):
        if not additional:
            additional = []
        document = Document.objects.get(pk=from_global_id(document_id)[1])
        document_unload: DocumentUnload = DocumentUnload(document, info.context.get_host(), additional)
        src: str = document_unload.xlsx()
        return UnloadDocumentMutation(src=src)


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
        # cell: Cell = Cell.objects.get(column_id=column_id, row_id=row_id)
        # В зависимости от типа применяем форматирование
        val, created = Value.objects.update_or_create(
            column_id=column_id,
            row_id=row_id,
            document=document,
            sheet=sheet,
            defaults={
                'value': value
            }
        )
        RowDimension.objects.filter(pk=row_id).update(updated_at=make_aware(datetime.now()))
        return ChangeValueMutation(value=val)


class DocumentMutations(graphene.ObjectType):
    """Мутации, связанные с документами."""

    add_document = AddDocumentMutation.Field(required=True)
    change_document_comment = ChangeDocumentCommentMutationPayload.Field(required=True)
    add_document_status = AddDocumentStatusMutation.Field(required=True)
    delete_document_status = DeleteDocumentStatusMutation.Field(required=True)
    unload_document = UnloadDocumentMutation.Field(required=True)

    change_value = ChangeValueMutation.Field(required=True)
