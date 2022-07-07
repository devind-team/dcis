from typing import Any, Optional

import graphene
from devind_core.schema.types import FileType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from graphene_django import DjangoListField
from graphql import ResolveInfo
from graphql_relay import from_global_id
from stringcase import snakecase

from apps.dcis.helpers.info_fields import get_fields
from apps.dcis.models import Sheet, Value
from apps.dcis.schema.types import SheetType
from apps.dcis.services.value_services import get_file_value_files
from apps.dcis.services.sheet_unload_services import SheetUploader


class SheetQueries(graphene.ObjectType):
    """Запросы записей, связанных с листами для вывода."""

    sheet = graphene.Field(
        SheetType,
        sheet_id=graphene.Int(required=True, description='Идентификатор листа'),
        document_id=graphene.ID(description='Идентификатор документа'),
        required=True,
        description='Выгрузка листа'
    )
    value_files = DjangoListField(
        FileType,
        document_id=graphene.ID(required=True, description='Идентификатор документа'),
        sheet_id=graphene.Int(required=True, description='Идентификатор листа'),
        column_id=graphene.Int(required=True, description='Идентификатор колонки'),
        row_id=graphene.Int(required=True, description='Идентификатор строки'),
        description='Файлы значения ячейки типа `Файл`'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_sheet(root: Any, info: ResolveInfo, sheet_id: str, document_id: Optional[str] = None):
        return SheetUploader(
            sheet=get_object_or_404(Sheet, pk=sheet_id),
            fields=[snakecase(k) for k in get_fields(info).keys() if k != '__typename'],
            document_id=from_global_id(document_id)[1] if document_id else None
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
        value = Value.objects.filter(
            document_id=from_global_id(document_id)[1],
            sheet_id=sheet_id,
            column_id=column_id,
            row_id=row_id
        ).first()
        if value is not None:
            return get_file_value_files(value)
        return []
