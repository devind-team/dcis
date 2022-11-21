from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.utils import gid2int
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
from apps.dcis.models import Attribute, Limitation, Period, Privilege, Sheet
from apps.dcis.permissions import can_change_period_sheet, can_view_period
from apps.dcis.schema.types import (
    AttributeType,
    DivisionModelTypeConnection,
    LimitationType,
    PeriodType,
    PrivilegeType,
    SheetType,
)
from apps.dcis.services.divisions_services import get_period_possible_divisions
from apps.dcis.services.period_services import (
    get_period_attributes,
    get_period_users,
    get_user_period_privileges,
    get_user_periods,
)
from apps.dcis.services.sheet_unload_services import DocumentsSheetUnloader, PeriodSheetUnloader


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

    period_sheet = graphene.Field(
        SheetType,
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        required=True,
        description='Выгрузка листа для периода'
    )
    documents_sheet = graphene.Field(
        SheetType,
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        document_ids=graphene.List(graphene.NonNull(graphene.ID), description='Идентификаторы документов'),
        required=True,
        description='Выгрузка листа с несколькими документами'
    )

    limitations = graphene.List(
        LimitationType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Ограничения, накладываемые на листы'
    )

    attributes = graphene.List(
        AttributeType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        parent=graphene.Boolean(default_value=True, description='Вытягивать только родителей'),
        required=True,
        description='Получение атрибутов, привязанных к периоду'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_privileges(root, info: ResolveInfo) -> QuerySet[Privilege]:
        return Privilege.objects.all()

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_period(root: Any, info: ResolveInfo, period_id: str) -> Period:
        period = get_object_or_404(Period, pk=from_global_id(period_id)[1])
        can_view_period(info.context.user, period)
        return period

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_periods(root: Any, info: ResolveInfo, project_id: str) -> QuerySet[Period]:
        return get_user_periods(info.context.user, from_global_id(project_id)[1])

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_period_possible_divisions(
        root: Any,
        info: ResolveInfo,
        period_id: str,
        search: str | None = None,
        *args,
        **kwargs
    ) -> list[dict[str, int | str]]:
        period = get_object_or_404(Period, pk=period_id)
        can_view_period(info.context.user, period)
        return get_period_possible_divisions(period, search or '')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_period_users(root: Any, info: ResolveInfo, period_id: str) -> QuerySet[User]:
        period = get_object_or_404(Period, pk=period_id)
        can_view_period(info.context.user, period)
        return get_period_users(period)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_user_period_privileges(
        root,
        info: ResolveInfo,
        user_id: str | None,
        period_id: str,
    ) -> QuerySet[Privilege]:
        period = get_object_or_404(Period, pk=period_id)
        can_view_period(info.context.user, period)
        user = get_user_from_id_or_context(info, user_id)
        return get_user_period_privileges(user.id, period.id)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_period_sheet(root: Any, info: ResolveInfo, sheet_id: str) -> list[dict] | dict:
        sheet = get_object_or_404(Sheet, pk=sheet_id)
        can_change_period_sheet(info.context.user, sheet.period)
        return PeriodSheetUnloader(
            sheet=sheet,
            fields=[snakecase(k) for k in get_fields(info).keys() if k != '__typename'],
        ).unload()

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_documents_sheet(
        root: Any,
        info: ResolveInfo,
        sheet_id: str,
        document_ids: list[str]
    ) -> list[dict] | dict:
        sheet = get_object_or_404(Sheet, pk=sheet_id)
        return DocumentsSheetUnloader(
            sheet=sheet,
            document_ids=[gid2int(document_id) for document_id in document_ids],
            fields=[snakecase(k) for k in get_fields(info).keys() if k != '__typename'],
        ).unload()

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_limitations(root: Any, info: ResolveInfo, period_id: str) -> QuerySet[Limitation]:
        period = get_object_or_404(Period, pk=gid2int(period_id))
        can_view_period(info.context.user, period)
        return Limitation.objects.filter(sheet__in=period.sheet_set.all())

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_attributes(
        root: Any,
        info: ResolveInfo,
        period_id: str,
        parent: bool = True
    ) -> QuerySet[Attribute]:
        period = get_object_or_404(Period, pk=gid2int(period_id))
        can_view_period(info.context.user, period)
        return get_period_attributes(period, parent=parent)
