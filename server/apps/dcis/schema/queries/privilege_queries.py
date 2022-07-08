import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.services.user_services import get_user_from_id_or_context
from apps.dcis.models import Period, Privilege
from apps.dcis.permissions import ViewPeriod
from apps.dcis.schema.types import PrivilegeType
from apps.dcis.services.period_services import get_user_individual_privileges


class PrivilegeQueries(graphene.ObjectType):
    """Запросы записей, связанных с привилегиями."""

    privileges = DjangoListField(
        PrivilegeType,
        required=True,
        description='Привилегии'
    )

    user_individual_privileges = DjangoListField(
        PrivilegeType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        user_id=graphene.ID(default_value=None, description='Идентификатор пользователя'),
        required=True,
        description='Отдельные привилегии пользователя для периода'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_privileges(root, info: ResolveInfo) -> QuerySet[Privilege]:
        return Privilege.objects.all()

    @staticmethod
    @permission_classes((IsAuthenticated, ViewPeriod,))
    def resolve_user_individual_privileges(
        root,
        info: ResolveInfo,
        period_id: str,
        user_id: str | None
    ) -> QuerySet[Privilege]:
        period = get_object_or_404(Period, pk=from_global_id(period_id)[1])
        info.context.check_object_permissions(info.context, period)
        user = get_user_from_id_or_context(info, user_id)
        return get_user_individual_privileges(user, period)
