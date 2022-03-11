import graphene
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import Document
from apps.dcis.schema.types import DocumentType


class DocumentQueries(graphene.ObjectType):
    """Запросы записей, связанных с документами."""

    document = graphene.Field(
        DocumentType,
        description='Документ',
        document_id=graphene.ID(description='Идентификатор документа')
    )

    @staticmethod
    def resolve_document(root, info: ResolveInfo, document_id: str, *args, **kwargs) -> None:
        return Document.objects.get(pk=from_global_id(document_id)[1])
