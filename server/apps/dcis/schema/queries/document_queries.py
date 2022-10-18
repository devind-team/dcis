from typing import Any

import graphene
from devind_core.schema import FileType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo
from devind_helpers.utils import gid2int
from stringcase import snakecase

from apps.dcis.helpers.info_fields import get_fields
from apps.dcis.models import Document, DocumentStatus, Sheet, Status, Value
from apps.dcis.permissions import can_view_document
from apps.dcis.schema.types import DocumentStatusType, DocumentType, SheetType, StatusType
from apps.dcis.services.document_services import get_user_documents
from apps.dcis.services.sheet_unload_services import DocumentSheetUnloader
from apps.dcis.services.value_services import get_file_value_files


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
        document_id=graphene.ID(required=True, description='Идентификатор документа')
    )

    statuses = DjangoListField(StatusType, description='Статусы')
    document_statuses = DjangoListField(
        DocumentStatusType,
        document_id=graphene.ID(description='Идентификатор документа'),
        description='Статусы документов'
    )

    document_sheet = graphene.Field(
        SheetType,
        document_id=graphene.ID(required=True, description='Идентификатор документа'),
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        required=True,
        description='Выгрузка листа с несколькими документами'
    )

    value_files = DjangoListField(
        FileType,
        document_id=graphene.ID(required=True, description='Идентификатор документа'),
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        column_id=graphene.ID(required=True, description='Идентификатор колонки'),
        row_id=graphene.ID(required=True, description='Идентификатор строки'),
        description='Файлы значения ячейки типа `Файл`'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_documents(root: Any, info: ResolveInfo, period_id: str, *args, **kwargs) -> QuerySet[Document]:
        return get_user_documents(info.context.user, gid2int(period_id))

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_document(root, info: ResolveInfo, document_id: str) -> Document:
        document = get_object_or_404(Document, pk=gid2int(document_id))
        can_view_document(info.context.user, document)
        return document

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_statuses(root, info: ResolveInfo) -> QuerySet[Status]:
        return Status.objects.all()

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_document_statuses(root, info: ResolveInfo, document_id: str) -> QuerySet[DocumentStatus]:
        document = get_object_or_404(Document, pk=gid2int(document_id))
        can_view_document(info.context.user, document)
        return document.documentstatus_set.all()

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_document_sheet(
        root,
        info: ResolveInfo,
        document_id: str,
        sheet_id: str
    ) -> list[dict] | dict:
        document = get_object_or_404(Document, pk=gid2int(document_id))
        can_view_document(info.context.user, document)
        return DocumentSheetUnloader(
            info.context,
            sheet=get_object_or_404(Sheet, pk=sheet_id),
            document_id=document.id,
            fields=[snakecase(k) for k in get_fields(info).keys() if k != '__typename'],
        ).unload()

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_value_files(
        root,
        info: ResolveInfo,
        document_id: str,
        sheet_id: str,
        column_id: str,
        row_id: str,
    ):
        document = get_object_or_404(Document, pk=gid2int(document_id))
        can_view_document(info.context.user, document)
        value = Value.objects.filter(
            document_id=document.id,
            sheet_id=sheet_id,
            column_id=column_id,
            row_id=row_id
        ).first()
        return get_file_value_files(value) if value is not None else []
