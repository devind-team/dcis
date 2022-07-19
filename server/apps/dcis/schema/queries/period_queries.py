from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from django.db.models import QuerySet
from graphene import ConnectionField
from graphene_django import DjangoListField
from graphql import ResolveInfo
from graphql_relay import from_global_id
from stringcase import snakecase

from apps.core.models import User
from apps.core.schema import UserType
from apps.core.services.user_services import get_user_from_id_or_context
from apps.dcis.helpers.info_fields import get_fields
from apps.dcis.models import Period, Privilege, Sheet
from apps.dcis.permissions import ChangePeriodSheet, ViewPeriod
from apps.dcis.schema.types import DivisionModelTypeConnection, PeriodType, PrivilegeType, SheetType
from apps.dcis.services.divisions_services import get_period_possible_divisions
from apps.dcis.services.period_services import (
    get_period_users,
    get_user_period_privileges,
    get_user_periods,
)
from apps.dcis.services.sheet_unload_services import DocumentsSheetUnloader


class PeriodQueries(graphene.ObjectType):
    """Запросы записей, связанных с периодами."""

    privileges = DjangoListField(
        PrivilegeType,
        required=True,
        description='Привилегии'
    )

    period = graphene.Field(
        PeriodType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Период'
    )
    periods = DjangoListField(
        PeriodType,
        project_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Периоды'
    )

    period_possible_divisions = ConnectionField(
        DivisionModelTypeConnection,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        search=graphene.String(description='Запрос поиска'),
        description='Возможные дивизионы периода'
    )

    period_users = DjangoListField(
        UserType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Пользователи, связанные периодом'
    )
    user_group_privileges = DjangoListField(
        PrivilegeType,
        user_id=graphene.ID(default_value=None, description='Идентификатор пользователя'),
        period_group_id=graphene.ID(required=True, description='Идентификатор группы периода'),
        required=True,
        description='Привилегии пользователя в группе периода'
    )
    user_period_privileges = DjangoListField(
        PrivilegeType,
        user_id=graphene.ID(default_value=None, description='Идентификатор пользователя'),
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Отдельные привилегии пользователя для периода'
    )

    documents_sheet = graphene.Field(
        SheetType,
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        document_ids=graphene.List(graphene.NonNull(graphene.ID), description='Идентификаторы документов'),
        required=True,
        description='Выгрузка листа с несколькими документами'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_privileges(root, info: ResolveInfo) -> QuerySet[Privilege]:
        return Privilege.objects.all()

    @staticmethod
    @permission_classes((IsAuthenticated, ViewPeriod))
    def resolve_period(root: Any, info: ResolveInfo, period_id: str) -> Period:
        period = get_object_or_404(Period, pk=from_global_id(period_id)[1])
        info.context.check_object_permissions(info.context, period)
        return period

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_periods(root: Any, info: ResolveInfo, project_id: str) -> QuerySet[Period]:
        return get_user_periods(info.context.user, from_global_id(project_id)[1])

    @staticmethod
    @permission_classes((IsAuthenticated, ViewPeriod,))
    def resolve_period_possible_divisions(
        root: Any,
        info: ResolveInfo,
        period_id: str,
        search: str | None = None,
        *args,
        **kwargs
    ) -> list[dict[str, int | str]]:
        period = get_object_or_404(Period, pk=period_id)
        info.context.check_object_permissions(info.context, period)
        return get_period_possible_divisions(period, search or '')

    @staticmethod
    @permission_classes((IsAuthenticated, ViewPeriod,))
    def resolve_period_users(root: Any, info: ResolveInfo, period_id: str) -> QuerySet[User]:
        period = get_object_or_404(Period, pk=period_id)
        info.context.check_object_permissions(info.context, period)
        return get_period_users(period)

    @staticmethod
    @permission_classes((IsAuthenticated, ViewPeriod,))
    def resolve_user_period_privileges(
        root,
        info: ResolveInfo,
        user_id: str | None,
        period_id: str,
    ) -> QuerySet[Privilege]:
        period = get_object_or_404(Period, pk=period_id)
        info.context.check_object_permissions(info.context, period)
        user = get_user_from_id_or_context(info, user_id)
        return get_user_period_privileges(user.id, period.id)

    @staticmethod
    @permission_classes((IsAuthenticated, ChangePeriodSheet,))
    def resolve_documents_sheet(
        root: Any,
        info: ResolveInfo,
        sheet_id: str,
        document_ids: list[str]
    ) -> list[dict] | dict:
        sheet = get_object_or_404(Sheet, pk=sheet_id)
        info.context.check_object_permissions(info.context, sheet.period)
        return DocumentsSheetUnloader(
            sheet=sheet,
            document_ids=[from_global_id(document_id)[1] for document_id in document_ids],
            fields=[snakecase(k) for k in get_fields(info).keys() if k != '__typename'],
        ).unload()
