import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.models import User
from apps.core.services.user_services import get_user_from_id_or_context
from apps.dcis.models import Period, PeriodGroup, Privilege
from apps.dcis.schema.types import PrivilegeType
from apps.dcis.services.period_services import get_user_group_privileges, get_user_period_privileges


class PrivilegeQueries(graphene.ObjectType):
    """Запросы записей, связанных с привилегиями."""

    privileges = DjangoListField(
        PrivilegeType,
        required=True,
        description='Привилегии'
    )

    user_group_privileges = DjangoListField(
        PrivilegeType,
        period_group_id=graphene.ID(required=True, description='Идентификатор группы'),
        user_id=graphene.ID(default_value=None, description='Идентификатор пользователя'),
        required=True,
        description='Привилегии назначенных пользователей периодов'
    )

    user_period_privileges = DjangoListField(
        PrivilegeType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        user_id=graphene.ID(default_value=None, description='Идентификатор пользователя'),
        required=True,
        description='Привилегии пользователя для периода'
    )

    additional_privileges = DjangoListField(
        PrivilegeType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        user_id=graphene.ID(required=True, description='Идентификатор пользователя'),
        required=True,
        description='Дополнительные личные привилегии'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_user_group_privileges(
            root,
            info: ResolveInfo,
            period_group_id: int,
            user_id: str | None = None
    ) -> QuerySet[Privilege]:
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        user: User = get_user_from_id_or_context(info, user_id)
        return get_user_group_privileges(user, period_group)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_user_period_privileges(
            root, info: ResolveInfo,
            period_id: str,
            user_id: str | None = None
    ) -> QuerySet[Privilege]:
        period = get_object_or_404(Period, pk=from_global_id(period_id)[1])
        user: User = get_user_from_id_or_context(info, user_id)
        return get_user_period_privileges(user, period)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_additional_privileges(
            root,
            info: ResolveInfo,
            period_id: str,
            user_id: str, *args, **kwargs) -> QuerySet[Privilege]:
        return Privilege.objects.filter(
            periodprivilege__user=from_global_id(user_id)[1],
            periodprivilege__period_id=period_id
        ).all()
