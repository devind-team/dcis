import graphene
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import PeriodPrivilege, Privilege
from apps.dcis.schema.types import PeriodPrivilegeType, PeriodGroupType, PrivilegeType


class PrivilegeQueries(graphene.ObjectType):
    """Запросы записей, связанных с привилегиями."""

    privileges = DjangoListField(
        PrivilegeType,
        required=True,
        description='Привилегии'
    )

    user_privileges = DjangoListField(
        PrivilegeType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        user_id=graphene.ID(required=True, description='Идентификатор пользователя'),
        required=True,
        description='Привилегии назначенных пользователей периодов'
    )

    @staticmethod
    def resolve_user_privileges(root, info: ResolveInfo, period_id: str, user_id: str, *args, **kwargs) -> QuerySet:
        return Privilege.objects.filter(periodprivilege__user_id=from_global_id(user_id)[1], periodprivilege__period_id=period_id).all()
