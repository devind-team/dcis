from typing import Any

import graphene
from devind_core.models import File
from devind_core.schema.types import FileType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from graphene_django import DjangoListField
from graphql import ResolveInfo

from apps.dcis.models import Sheet
from apps.dcis.schema.types import Value, SheetType
from apps.dcis.services.value import get_file_value_files


class SheetQueries(graphene.ObjectType):
    """Запросы записей, связанных с листами для вывода."""

    value_files = DjangoListField(
        FileType,
        description='Файлы значения ячейки типа `Файл`',
        value_id=graphene.ID(required=True, description='Идентификатор значения ячейки')

    sheet = graphene.Field(
        SheetType,
        sheet_id=graphene.Int(required=True, description='Идентификатор листа'),
        required=True,
        description='Выгрузка листа'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_value_files(root, info: ResolveInfo, value_id: str) -> list[File]:
        return get_file_value_files(get_object_or_404(Value, pk=value_id))

    def resolve_sheet(root: Any, info: ResolveInfo, sheet_id: int):
        return get_object_or_404(Sheet, pk=sheet_id)
