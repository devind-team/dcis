from typing import Any

import graphene
from devind_helpers.orm_utils import get_object_or_404
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import Document, DocumentStatus
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
    def resolve_documents(root: Any, info: ResolveInfo, period_id: str) -> QuerySet[Document]:
        return get_user_documents(info.context.user, from_global_id(period_id)[1])

    @staticmethod
    def resolve_document(root, info: ResolveInfo, document_id: str) -> Document:
        return get_object_or_404(Document, pk=from_global_id(document_id)[1])

    @staticmethod
    def resolve_document_statuses(root, info: ResolveInfo, document_id: str) -> QuerySet:
        return DocumentStatus.objects.filter(document_id=from_global_id(document_id)[1]).all()
