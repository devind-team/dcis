from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from graphene_django import DjangoListField
from graphql import ResolveInfo

from apps.dcis.models import CuratorGroup
from apps.dcis.schema.types import (
    CuratorGroupType,
)


class CuratorGroupQueries(graphene.ObjectType):
    """Запросы записей, связанных с группами кураторов."""

    curator_groups: CuratorGroup = DjangoListField(
        CuratorGroupType,
        required=True,
        description='Кураторские группы'
    )

    curator_group: CuratorGroup = graphene.Field(
        CuratorGroupType,
        curator_group_id=graphene.ID(required=True, description='Идентификатор кураторской группы'),
        required=True,
        description='Кураторская группа'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_curator_group(root: Any, info: ResolveInfo, curator_group_id: str) -> CuratorGroup:
        curator_group: CuratorGroup = get_object_or_404(CuratorGroup, pk=curator_group_id)
        return curator_group
