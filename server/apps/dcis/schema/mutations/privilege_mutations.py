from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.models import User
from apps.dcis.models import Period, PeriodGroup, PeriodPrivilege, Privilege
from apps.dcis.schema.types import PrivilegeType


class ChangePeriodGroupPrivilegesMutation(BaseMutation):
    """Мутация на изменение привилегий группы."""

    class Input:
        period_group_id = graphene.Int(required=True, description='Идентификатор группы периода')
        privileges_ids = graphene.List(graphene.NonNull(graphene.ID), description='Привилегии')

    privileges = graphene.List(PrivilegeType, required=True, description='Привилегии группы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_group_id: int, privileges_ids: list[str]):
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        privileges: list[Privilege] = []
        for privilege_id in privileges_ids:
            privilege = get_object_or_404(Privilege, pk=privilege_id)
            privileges.append(privilege)
        period_group.privileges.set(privileges)
        return ChangePeriodGroupPrivilegesMutation(privileges=privileges)


class ChangeGroupUserPrivilegesMutation(BaseMutation):
    """Мутация на изменение привилегий пользователя."""

    class Input:
        period_group_id = graphene.ID(required=True, description='Идентификатор группы периода')
        user_id = graphene.ID(required=True, description='Идентификатор группы периода')
        privileges_ids = graphene.List(graphene.NonNull(graphene.ID), description='Привилегии')

    privileges = graphene.List(PrivilegeType, required=True, description='Привилегии пользователя')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        period_group_id: str,
        user_id: str,
        privileges_ids: list[str]
    ):
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        period = get_object_or_404(Period, pk=period_group.period.id)
        user = get_object_or_404(User, pk=from_global_id(user_id)[1])
        period_privileges = PeriodPrivilege.objects.filter(user=user, period=period)
        privileges = period_privileges.values_list('privilege', flat=True)
        for period_privilege in period_privileges:
            if period_privilege.privilege.id not in privileges_ids:
                period_privilege.delete()
        for privilege_id in privileges_ids:
            if privilege_id not in privileges:
                PeriodPrivilege.objects.create(user=user, period=period, privilege_id=privilege_id)
        user_privileges = Privilege.objects.filter(periodprivilege__user=user, periodprivilege__period=period)
        return ChangePeriodGroupPrivilegesMutation(
            privileges=user_privileges | Privilege.objects.filter(periodgroup=period_group).all()
        )


class PrivilegeMutations(graphene.ObjectType):
    """Список мутация привилегий."""

    change_period_group_privileges = ChangePeriodGroupPrivilegesMutation.Field(required=True)
    change_group_users_privileges = ChangeGroupUserPrivilegesMutation.Field(required=True)
