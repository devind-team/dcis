from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.exceptions import PermissionDenied
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from graphene_django_cud.mutations import DjangoUpdateMutation
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.models import User
from apps.dcis.models import Document, DocumentStatus, Period, Status
from apps.dcis.permissions import AddDocument, ChangeDocument
from apps.dcis.schema.types import DocumentStatusType, DocumentType
from apps.dcis.services.document_services import create_new_document
from apps.dcis.services.document_unload_services import DocumentUnload


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
        document_id: int | None = None,
        division_id: int | None = None,
    ) -> 'AddDocumentMutation':
        """Мутация для добавления документа."""
        user: User = info.context.user
        period: Period = get_object_or_404(Period, pk=period_id)
        info.context.check_object_permissions(info.context, period)
        document_id: int | None = from_global_id(document_id)[1] if document_id else None
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

    @classmethod
    def check_permissions(cls, root: Any, info: ResolveInfo, input: Any, id: str, obj: Document) -> None:
        if not ChangeDocument.has_object_permission(info.context, obj):
            raise PermissionDenied('Ошибка доступа')


class AddDocumentStatusMutation(BaseMutation):
    """Добавление статуса документа."""

    class Input:
        document_id = graphene.ID(required=True, description='Документ')
        status_id = graphene.Int(required=True, description='Статус')
        comment = graphene.String(description='Комментарий')

    document_status = graphene.Field(DocumentStatusType, description='Статус документа')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangeDocument))
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_id: str, status_id: int, comment: str):
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        info.context.check_object_permissions(info.context, document)
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
    @permission_classes((IsAuthenticated, ChangeDocument,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_status_id: int):
        status = get_object_or_404(DocumentStatus, pk=document_status_id)
        info.context.check_object_permissions(info.context, status.document)
        status.delete()
        return DeleteDocumentStatusMutation(id=document_status_id)


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
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_id: str, additional: list[str] | None = None):
        if not additional:
            additional = []
        document = Document.objects.get(pk=from_global_id(document_id)[1])
        document_unload: DocumentUnload = DocumentUnload(document, info.context.get_host(), additional)
        src: str = document_unload.xlsx()
        return UnloadDocumentMutation(src=src)


class DocumentMutations(graphene.ObjectType):
    """Мутации, связанные с документами."""

    add_document = AddDocumentMutation.Field(required=True)
    change_document_comment = ChangeDocumentCommentMutationPayload.Field(required=True)
    add_document_status = AddDocumentStatusMutation.Field(required=True)
    delete_document_status = DeleteDocumentStatusMutation.Field(required=True)
    unload_document = UnloadDocumentMutation.Field(required=True)
