from typing import Any

import graphene
from devind_dictionaries.models import Organization
from devind_dictionaries.schema import OrganizationType
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
from apps.dcis.models import Attribute, Document, Limitation, Period, Privilege, Sheet
from apps.dcis.permissions import can_change_period_sheet, can_view_period, can_view_period_result
from apps.dcis.schema.types import (
    AttributeType,
    DivisionModelTypeConnection,
    LimitationType,
    PeriodType,
    PrivilegeType,
    ReportDocumentInputType,
    ReportRowGroupInputType,
    SheetType,
)
from apps.dcis.services.divisions_services import get_period_possible_divisions
from apps.dcis.services.period_services import (
    get_organizations_has_not_document, get_period_attributes,
    get_period_users,
    get_user_period_privileges,
    get_user_periods,
)
from apps.dcis.services.row_dimension_services import get_indices_groups_to_expand
from apps.dcis.services.sheet_unload_services import (
    PeriodSheetUnloader,
    ReportAggregation,
    ReportDocument,
    ReportSheetUnloader,
)


class PeriodQueries(graphene.ObjectType):
    """Запросы записей, связанных с периодами."""

    privileges = DjangoListField(
        PrivilegeType,
        required=True,
        description='Привилегии',
    )

    period = graphene.Field(
        PeriodType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Период',
    )
    periods = DjangoListField(
        PeriodType,
        project_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Периоды',
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
        description='Пользователи, связанные периодом',
    )
    user_group_privileges = DjangoListField(
        PrivilegeType,
        user_id=graphene.ID(default_value=None, description='Идентификатор пользователя'),
        period_group_id=graphene.ID(required=True, description='Идентификатор группы периода'),
        required=True,
        description='Привилегии пользователя в группе периода',
    )
    user_period_privileges = DjangoListField(
        PrivilegeType,
        user_id=graphene.ID(default_value=None, description='Идентификатор пользователя'),
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Отдельные привилегии пользователя для периода',
    )

    period_sheet = graphene.Field(
        SheetType,
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        required=True,
        description='Выгрузка листа для периода',
    )

    indices_groups_to_expand = graphene.List(
        graphene.NonNull(graphene.List(graphene.NonNull(graphene.Int))),
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        description='Группы индексов строк, которые можно расширить'
    )
    report_sheet = graphene.Field(
        SheetType,
        sheet_id=graphene.ID(required=True, description='Идентификатор листа'),
        report_documents=graphene.List(
            graphene.NonNull(ReportDocumentInputType),
            required=True,
            description='Документы для выгрузки сводного отчета',
        ),
        report_row_groups=graphene.List(
            graphene.NonNull(ReportRowGroupInputType),
            required=True,
            description='Группы строк для выгрузки сводного отчета',
        ),
        main_document_id=graphene.ID(description='Основной документ'),
        aggregation=graphene.Argument(
            graphene.Enum.from_enum(ReportAggregation),
            description='Тип агрегации для сводного отчета',
        ),
        required=True,
        description='Выгрузка листа для сводного отчета',
    )

    limitations = graphene.List(
        LimitationType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Ограничения, накладываемые на листы',
    )

    attributes = graphene.List(
        AttributeType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        parent=graphene.Boolean(default_value=True, description='Вытягивать только родителей'),
        required=True,
        description='Получение атрибутов, привязанных к периоду',
    )

    organizations_has_not_document = graphene.List(
        OrganizationType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Получение организаций, у которых не поданы документы в периоде'
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
    def resolve_indices_groups_to_expand(root: Any, info: ResolveInfo, sheet_id: str) -> list[list[int]]:
        sheet = get_object_or_404(Sheet, pk=gid2int(sheet_id))
        can_view_period_result(info.context.user, sheet.period)
        return get_indices_groups_to_expand(sheet)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_report_sheet(
        root: Any,
        info: ResolveInfo,
        sheet_id: str,
        report_documents: list[ReportDocumentInputType],
        report_row_groups: list[ReportRowGroupInputType],
        **kwargs
    ) -> list[dict] | dict:
        sheet = get_object_or_404(Sheet, pk=gid2int(sheet_id))
        can_view_period_result(info.context.user, sheet.period)
        if 'main_document_id' in kwargs:
            main_document = get_object_or_404(Document, pk=gid2int(kwargs['main_document_id']))
        else:
            main_document = None
        aggregation = ReportAggregation(kwargs['aggregation']) if 'aggregation' in kwargs else None
        document_ids = [gid2int(report_document.document_id) for report_document in report_documents]
        documents = Document.objects.filter(id__in=document_ids)
        expanded_row_groups = {}
        for group in report_row_groups:
            expanded_row_groups[group.group_index] = group.is_expanded
        return ReportSheetUnloader(
            sheet=sheet,
            report_documents=[next(
                ReportDocument(document=d, is_visible=r.is_visible, color=r.color)
                for r in report_documents if gid2int(r.document_id) == d.id
            ) for d in documents],
            main_document=main_document,
            aggregation=aggregation,
            expanded_row_groups=expanded_row_groups,
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

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_organizations_has_not_document(root: Any, info: ResolveInfo, period_id: str) -> QuerySet[Organization]:
        period = get_object_or_404(Period, pk=gid2int(period_id))
        return get_organizations_has_not_document(info.context.user, period)
