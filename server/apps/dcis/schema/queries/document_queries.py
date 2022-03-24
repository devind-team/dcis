import graphene
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphql import ResolveInfo
from graphql_relay import from_global_id
from devind_helpers.orm_utils import get_object_or_404

from apps.dcis.models import Document, DocumentStatus
from apps.dcis.schema.types import DocumentType, StatusType, DocumentStatusType


class DocumentQueries(graphene.ObjectType):
    """Запросы записей, связанных с документами."""

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
    def resolve_document(root, info: ResolveInfo, document_id: str, *args, **kwargs) -> None:
        return Document.objects.get(pk=from_global_id(document_id)[1])

    @staticmethod
    def resolve_document_statuses(root, info: ResolveInfo, document_id: str, *args, **kwargs) -> QuerySet:
        return DocumentStatus.objects.filter(document_id=from_global_id(document_id)[1])
