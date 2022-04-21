import graphene
from devind_core.models import File
from devind_core.schema.types import FileType
from devind_helpers.decorators import permission_classes
from devind_helpers.permissions import IsAuthenticated
from graphene_django import DjangoListField
from graphql import ResolveInfo

from apps.dcis.schema.types import Value
from apps.dcis.services.cell import get_file_value_files, get_file_value_archive_url


class SheetQueries(graphene.ObjectType):
    """Запросы записей, связанных с листами для вывода."""

    value_archive_file = graphene.String()
    value_files = DjangoListField(
        FileType,
        description='Файлы значения ячейки',
        value_id=graphene.ID(description='Идентификатор значения ячейки')
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_value_archive_file(root, info: ResolveInfo, value_id) -> str:
        return get_file_value_archive_url(Value.objects.get(pk=value_id))

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_value_files(root, info: ResolveInfo, value_id: str) -> list[File]:
        return get_file_value_files(Value.objects.get(pk=value_id))
