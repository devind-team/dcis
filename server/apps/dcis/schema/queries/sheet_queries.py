from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from graphql import ResolveInfo

from apps.dcis.models import Sheet
from apps.dcis.schema.types import SheetType


class SheetQueries(graphene.ObjectType):
    """Запросы записей, связанных с листами для вывода."""

    sheet = graphene.Field(
        SheetType,
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        required=True,
        description='Выгрузка листа'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_sheet(root: Any, info: ResolveInfo, sheet_id: int):
        return get_object_or_404(Sheet, pk=sheet_id)
