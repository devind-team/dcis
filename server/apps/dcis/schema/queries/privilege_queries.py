import graphene
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import PeriodPrivilege
from apps.dcis.schema.types import PeriodPrivilegeType, PeriodGroupType


class PrivilegeQueries(graphene.ObjectType):
    """Запросы записей, связанных с привилегиями."""

    period_privileges = DjangoListField(
        PeriodPrivilegeType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        user_id=graphene.ID(required=True, description='Идентификатор пользователя'),
        required=True,
        description='Привилегии назначенных пользователей периодов'
    )

    @staticmethod
    def resolve_period_privileges(root, info: ResolveInfo, period_id: int, user_id: str, *args, **kwargs) -> QuerySet:
        return PeriodPrivilege.objects.filter(period_id=period_id, user_id=from_global_id(user_id)[1]).all()
