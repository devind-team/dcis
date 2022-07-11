from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import Document, DocumentStatus, Status
from apps.dcis.permissions import ViewDocument
from apps.dcis.schema.types import DocumentStatusType, DocumentType, StatusType
from apps.dcis.services.document_services import get_user_documents


class DocumentQueries(graphene.ObjectType):
    """Запросы записей, связанных с документами."""
    documents = DjangoFilterConnectionField(
        DocumentType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Документы'
    )
    document = graphene.Field(
        DocumentType,
        description='Документ',
        document_id=graphene.ID(description='Идентификатор документа')
    )

    statuses = DjangoListField(StatusType, description='Статусы')
    document_statuses = DjangoListField(
        DocumentStatusType,
        document_id=graphene.ID(description='Идентификатор документа'),
        description='Статусы документов'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_documents(root: Any, info: ResolveInfo, period_id: str) -> QuerySet[Document]:
        return get_user_documents(info.context.user, from_global_id(period_id)[1])

    @staticmethod
    @permission_classes((IsAuthenticated, ViewDocument,))
    def resolve_document(root, info: ResolveInfo, document_id: str) -> Document:
        document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        info.context.check_object_permissions(info.context, document)
        return document

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_statuses(root, info: ResolveInfo) -> QuerySet[Status]:
        return Status.objects.all()

    @staticmethod
    @permission_classes((IsAuthenticated, ViewDocument,))
    def resolve_document_statuses(root, info: ResolveInfo, document_id: str) -> QuerySet[DocumentStatus]:
        document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        info.context.check_object_permissions(info.context, document)
        return document.documentstatus_set.all()
