from typing import Any

import graphene
from devind_helpers.orm_utils import get_object_or_404
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import Document, DocumentStatus
from apps.dcis.schema.types import DocumentType, StatusType, DocumentStatusType
from apps.dcis.services.document_services import get_documents


class DocumentQueries(graphene.ObjectType):
    """Запросы записей, связанных с документами."""
    documents = DjangoFilterConnectionField(
        DocumentType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        divisions_id=graphene.List(graphene.NonNull(graphene.Int), description='Идентификаторы дивизионов'),
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
    def resolve_documents(root: Any, info: ResolveInfo, period_id: str, divisions_id: list[str] = []):
        period_id: int = from_global_id(period_id)[1]
        return get_documents(info.context.user, period_id, divisions_id)

    @staticmethod
    def resolve_document(root, info: ResolveInfo, document_id: str, *args, **kwargs) -> Document:
        return get_object_or_404(Document, pk=from_global_id(document_id)[1])

    @staticmethod
    def resolve_document_statuses(root, info: ResolveInfo, document_id: str, *args, **kwargs) -> QuerySet:
        return DocumentStatus.objects.filter(document_id=from_global_id(document_id)[1]).all()
