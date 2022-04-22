import graphene
from devind_core.models import File
from devind_core.schema.types import FileType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from graphene_django import DjangoListField
from graphql import ResolveInfo

from apps.dcis.schema.types import Value
from apps.dcis.services.value import get_file_value_files_url, get_file_value_files


class SheetQueries(graphene.ObjectType):
    """Запросы записей, связанных с листами для вывода."""

    value_files_url = graphene.String(
        description='URL файла или архива значения ячейки типа `Файл`',
        value_id=graphene.ID(required=True, description='Идентификатор значения ячейки')
    )
    value_files = DjangoListField(
        FileType,
        description='Файлы значения ячейки типа `Файл`',
        value_id=graphene.ID(required=True, description='Идентификатор значения ячейки')
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_value_files_url(root, info: ResolveInfo, value_id: str) -> str:
        return get_file_value_files_url(get_object_or_404(Value, pk=value_id))

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_value_files(root, info: ResolveInfo, value_id: str) -> list[File]:
        return get_file_value_files(get_object_or_404(Value, pk=value_id))
