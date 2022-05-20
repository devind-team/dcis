import graphene
from devind_helpers.orm_utils import get_object_or_404
from graphene_django import DjangoListField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.models import User
from apps.dcis.models import Privilege, PeriodGroup
from apps.dcis.schema.types import PrivilegeType


class PrivilegeQueries(graphene.ObjectType):
    """Запросы записей, связанных с привилегиями."""

    privileges = DjangoListField(
        PrivilegeType,
        required=True,
        description='Привилегии'
    )

    user_privileges = DjangoListField(
        PrivilegeType,
        period_group_id=graphene.ID(required=True, description='Идентификатор группы'),
        user_id=graphene.ID(required=True, description='Идентификатор пользователя'),
        required=True,
        description='Привилегии назначенных пользователей периодов'
    )

    @staticmethod
    def resolve_user_privileges(root, info: ResolveInfo, period_group_id: str, user_id: str, *args,
                                **kwargs) -> set[Privilege]:
        user = get_object_or_404(User, pk=from_global_id(user_id)[1])
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        user_privileges = Privilege.objects.filter(periodprivilege__user=user,
                                                   periodprivilege__period=period_group.period.id).all()
        group_privileges = Privilege.objects.filter(periodgroup=period_group, periodgroup__users=user)
        privileges = set(list(user_privileges) + list(group_privileges))
        return privileges
