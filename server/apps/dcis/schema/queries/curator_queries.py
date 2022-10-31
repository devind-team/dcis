from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo

from apps.core.models import User
from apps.core.schema import UserType
from apps.dcis.models import CuratorGroup
from apps.dcis.permissions.curator_permissions import can_view_curator_group
from apps.dcis.schema.types import CuratorGroupType
from apps.dcis.services.curator_services import get_curator_group_new_users


class CuratorGroupQueries(graphene.ObjectType):
    """Запросы записей, связанных с группами кураторов."""

    curator_groups = DjangoListField(
        CuratorGroupType,
        required=True,
        description='Кураторские группы'
    )
    curator_group = graphene.Field(
        CuratorGroupType,
        curator_group_id=graphene.ID(required=True, description='Идентификатор кураторской группы'),
        required=True,
        description='Кураторская группа'
    )
    curator_group_new_users = DjangoFilterConnectionField(
        UserType,
        curator_group_id=graphene.ID(required=True, description='Идентификатор кураторской группы'),
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_curator_groups(root: Any, info: ResolveInfo) -> QuerySet[CuratorGroup]:
        can_view_curator_group(info.context.user)
        return CuratorGroup.objects.all()

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_curator_group(root: Any, info: ResolveInfo, curator_group_id: str) -> CuratorGroup:
        curator_group = get_object_or_404(CuratorGroup, pk=curator_group_id)
        can_view_curator_group(info.context.user)
        return curator_group

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_curator_group_new_users(
        root: Any,
        info: ResolveInfo,
        curator_group_id: str,
        *args,
        **kwargs,
    ) -> QuerySet[User]:
        can_view_curator_group(info.context.user)
        return get_curator_group_new_users(curator_group_id)
