from typing import Any, Optional

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from graphql import ResolveInfo
from graphql_relay import from_global_id
from stringcase import snakecase

from apps.dcis.helpers.info_fields import get_fields
from apps.dcis.models import Sheet
from apps.dcis.schema.types import SheetType
from apps.dcis.services.sheet_unload_services import SheetUploader


class SheetQueries(graphene.ObjectType):
    """Запросы записей, связанных с листами для вывода."""

    sheet = graphene.Field(
        SheetType,
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        document_id=graphene.ID(description='Идентификатор документа'),
        required=True,
        description='Выгрузка листа'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_sheet(root: Any, info: ResolveInfo, sheet_id: str, document_id: Optional[str] = None):
        return SheetUploader(
            sheet=get_object_or_404(Sheet, pk=sheet_id),
            fields=[snakecase(k) for k in get_fields(info).keys() if k != '__typename'],
            document_id=from_global_id(document_id)[1] if document_id else None
        ).unload()
