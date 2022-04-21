from typing import cast

import graphene
from devind_core.models import File
from devind_core.schema.types import FileType
from graphene_django import DjangoListField
from graphql import ResolveInfo

from apps.dcis.schema.types import Value


class SheetQueries(graphene.ObjectType):
    """Запросы записей, связанных с листами для вывода."""

    value_files = DjangoListField(
        FileType,
        description='Файлы значения ячейки',
        value_id=graphene.ID(description='Идентификатор значения ячейки')
    )

    @staticmethod
    def resolve_value_files(root, info: ResolveInfo, value_id: str) -> list[File]:
        value = Value.objects.get(pk=value_id)
        if value.payload is None:
            return []
        payload = cast(list[int], value.payload)
        files = File.objects.filter(pk__id=payload)
        return sorted(files, key=lambda file: payload.index(file.pk))
