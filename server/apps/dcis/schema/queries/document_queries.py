from typing import Any, Iterable

import graphene
import graphene_django_optimizer as gql_optimizer
from devind_core.models import File
from devind_core.schema import FileType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.utils import gid2int
from graphene_django import DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo
from stringcase import snakecase

from apps.dcis.helpers.info_fields import get_fields
from apps.dcis.models import (
    AttributeValue,
    Cell,
    Document,
    DocumentMessage,
    DocumentStatus,
    Period,
    Sheet,
    Status,
    Value,
)
from apps.dcis.ordering import DocumentOrderedDjangoFilterConnectionField
from apps.dcis.permissions import can_view_document
from apps.dcis.schema.types import (
    AddStatusType,
    AttributeValueType,
    CellAggregationType,
    ChangeCellType,
    DocumentMessageType,
    DocumentStatusType,
    DocumentType,
    SheetType,
    StatusType,
)
from apps.dcis.services.aggregation_services import CellsAggregation, get_cells_aggregation
from apps.dcis.services.document_services import get_user_documents
from apps.dcis.services.sheet_services import get_aggregation_cells
from apps.dcis.services.sheet_unload_services import DocumentSheetUnloader
from apps.dcis.services.status_services import get_initial_statuses, get_new_statuses
from apps.dcis.services.value_services import get_file_value_files


class DocumentQueries(graphene.ObjectType):
    """Запросы записей, связанных с документами."""
    documents = DocumentOrderedDjangoFilterConnectionField(
        DocumentType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Документы',
    )
    document = graphene.Field(
        DocumentType,
        description='Документ',
        document_id=graphene.ID(required=True, description='Идентификатор документа'),
    )

    document_messages = DjangoFilterConnectionField(
        DocumentMessageType,
        document_id=graphene.ID(required=True, description='Идентификатор документа'),
        description='Комментарии документов'
    )

    statuses = DjangoListField(StatusType, description='Статусы')
    add_statuses = DjangoListField(AddStatusType, description='Переназначение статусов')
    initial_statuses = DjangoListField(
        StatusType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        description='Возможные начальные статусы для нового документа',
    )
    new_statuses = DjangoListField(
        StatusType,
        document_id=graphene.ID(required=True, description='Идентификатор документа'),
        description='Возможные новые статусы для документа',
    )
    document_statuses = DjangoListField(
        DocumentStatusType,
        document_id=graphene.ID(description='Идентификатор документа'),
        description='Статусы документов',
    )

    attributes_values = graphene.List(
        AttributeValueType,
        document_id=graphene.ID(required=True, description='Идентификатор документа'),
        required=True,
        description='Атрибуты со значениями документа'
    )

    document_sheet = graphene.Field(
        SheetType,
        document_id=graphene.ID(required=True, description='Идентификатор документа'),
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        required=True,
        description='Выгрузка листа с несколькими документами',
    )

    value_files = DjangoListField(
        FileType,
        document_id=graphene.ID(required=True, description='Идентификатор документа'),
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        column_id=graphene.ID(required=True, description='Идентификатор колонки'),
        row_id=graphene.ID(required=True, description='Идентификатор строки'),
        description='Файлы значения ячейки типа `Файл`',
    )

    value_cells = graphene.List(
        ChangeCellType,
        cell_id=graphene.ID(required=True, description='Идентификатор ячейки'),
        description='Ячейка и ее зависимости'
    )

    aggregation_cells = graphene.List(
        CellAggregationType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        description='Агрегированные ячейки документов периода'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_documents(root: Any, info: ResolveInfo, period_id: str, *args, **kwargs) -> Iterable[Document]:
        return gql_optimizer.query(get_user_documents(info.context.user, gid2int(period_id)), info)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_document(root: Any, info: ResolveInfo, document_id: str) -> Document:
        document = get_object_or_404(Document, pk=gid2int(document_id))
        can_view_document(info.context.user, document)
        return document

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_document_messages(
        root: Any,
        info: ResolveInfo,
        document_id: str,
        *args,
        **kwarg
    ) -> Iterable[DocumentMessage]:
        document = get_object_or_404(Document, pk=gid2int(document_id))
        can_view_document(info.context.user, document)
        return DocumentMessage.objects.filter(document=document)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_statuses(root: Any, info: ResolveInfo) -> Iterable[Status]:
        return Status.objects.all()

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_initial_statuses(root: Any, info: ResolveInfo, period_id: str) -> Iterable[Status]:
        period = get_object_or_404(Period, pk=period_id)
        return get_initial_statuses(info.context.user, period)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_new_statuses(root: Any, info: ResolveInfo, document_id: str) -> Iterable[Status]:
        document = get_object_or_404(Document, pk=gid2int(document_id))
        return get_new_statuses(info.context.user, document)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_document_statuses(root: Any, info: ResolveInfo, document_id: str) -> Iterable[DocumentStatus]:
        document = get_object_or_404(Document, pk=gid2int(document_id))
        can_view_document(info.context.user, document)
        return document.documentstatus_set.all()

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_attributes_values(
        root: Any,
        info: ResolveInfo,
        document_id: str
    ) -> Iterable[AttributeValue]:
        document: Document = Document.objects.get(pk=gid2int(document_id))
        can_view_document(info.context.user, document)
        return AttributeValue.objects.filter(document=document).all()

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_document_sheet(
        root: Any,
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
        root: Any,
        info: ResolveInfo,
        document_id: str,
        sheet_id: str,
        column_id: str,
        row_id: str,
    ) -> Iterable[File]:
        document = get_object_or_404(Document, pk=gid2int(document_id))
        can_view_document(info.context.user, document)
        value = Value.objects.filter(
            document_id=document.id,
            sheet_id=sheet_id,
            column_id=column_id,
            row_id=row_id
        ).first()
        return get_file_value_files(value) if value is not None else []

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_value_cells(root, info: ResolveInfo, cell_id: str) -> list[Cell]:
        cell = get_object_or_404(Cell, pk=gid2int(cell_id))
        return get_aggregation_cells(info.context.user, cell)


    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_aggregation_cells(root, info: ResolveInfo, period_id: str | int) -> list[CellsAggregation]:
        period = get_object_or_404(Period, pk=gid2int(period_id))
        return get_cells_aggregation(info.context.user, period)
