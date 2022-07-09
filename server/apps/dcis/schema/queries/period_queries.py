from typing import Any

import graphene
from devind_core.schema.types import FileType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphql import ResolveInfo
from graphql_relay import from_global_id
from stringcase import snakecase

from apps.core.models import User
from apps.core.schema import UserType
from apps.core.services.user_services import get_user_from_id_or_context
from apps.dcis.helpers.info_fields import get_fields
from apps.dcis.models import Period, PeriodGroup, Privilege, Sheet, Value
from apps.dcis.permissions import ViewPeriod
from apps.dcis.schema.types import PeriodType, PrivilegeType, SheetType
from apps.dcis.services.period_services import (
    get_period_users,
    get_user_group_privileges,
    get_user_individual_privileges,
    get_user_periods,
)
from apps.dcis.services.sheet_services import get_file_value_files
from apps.dcis.services.sheet_unload_services import SheetUploader


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
    user_individual_privileges = DjangoListField(
        PrivilegeType,
        user_id=graphene.ID(default_value=None, description='Идентификатор пользователя'),
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Отдельные привилегии пользователя для периода'
    )

    sheet = graphene.Field(
        SheetType,
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        document_id=graphene.ID(description='Идентификатор документа'),
        required=True,
        description='Выгрузка листа'
    )
    value_files = DjangoListField(
        FileType,
        document_id=graphene.ID(required=True, description='Идентификатор документа'),
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        column_id=graphene.ID(required=True, description='Идентификатор колонки'),
        row_id=graphene.ID(required=True, description='Идентификатор строки'),
        description='Файлы значения ячейки типа `Файл`'
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
    def resolve_period_users(root: Any, info: ResolveInfo, period_id: str) -> QuerySet[User]:
        period = get_object_or_404(Period, pk=period_id)
        info.context.check_object_permissions(info.context, period)
        return get_period_users(period)

    @staticmethod
    @permission_classes((IsAuthenticated, ViewPeriod,))
    def resolve_user_group_privileges(
        root,
        info: ResolveInfo,
        user_id: str | None,
        period_group_id: str
    ) -> QuerySet[Privilege]:
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        info.context.check_object_permissions(info.context, period_group.period)
        user = get_user_from_id_or_context(info, user_id)
        return get_user_group_privileges(user.id, period_group.id)

    @staticmethod
    @permission_classes((IsAuthenticated, ViewPeriod,))
    def resolve_user_individual_privileges(
        root,
        info: ResolveInfo,
        user_id: str | None,
        period_id: str,
    ) -> QuerySet[Privilege]:
        period = get_object_or_404(Period, pk=period_id)
        info.context.check_object_permissions(info.context, period)
        user = get_user_from_id_or_context(info, user_id)
        return get_user_individual_privileges(user.id, period.id)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_sheet(root: Any, info: ResolveInfo, sheet_id: str, document_id: str | None = None):
        return SheetUploader(
            sheet=get_object_or_404(Sheet, pk=sheet_id),
            fields=[snakecase(k) for k in get_fields(info).keys() if k != '__typename'],
            document_id=from_global_id(document_id)[1] if document_id else None
        ).unload()

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_value_files(
        root,
        info: ResolveInfo,
        document_id: str,
        sheet_id: str,
        column_id: str,
        row_id: str,
    ):
        value = Value.objects.filter(
            document_id=from_global_id(document_id)[1],
            sheet_id=sheet_id,
            column_id=column_id,
            row_id=row_id
        ).first()
        if value is not None:
            return get_file_value_files(value)
        return []
