from typing import Any

import graphene
from devind_dictionaries.models import Department, Organization
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphene_django_filter import AdvancedDjangoFilterConnectionField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.models import User
from apps.dcis.models import Period, Project
from apps.dcis.permissions import ViewPeriod, ViewProject
from apps.dcis.schema.types import DivisionModelType, PeriodType, ProjectType
from apps.dcis.services.divisions_services import get_user_divisions
from apps.dcis.services.period_services import get_user_periods
from apps.dcis.services.project_services import get_user_projects


class ProjectQueries(graphene.ObjectType):
    """Запросы записей, связанных с проектами."""

    project = graphene.Field(
        ProjectType,
        project_id=graphene.ID(required=True, description='Идентификатор проекта'),
        required=True,
        description='Проект'
    )
    projects = AdvancedDjangoFilterConnectionField(ProjectType, description='Проекты')

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

    user_divisions = graphene.List(
        DivisionModelType,
        user_id=graphene.ID(description='Пользователь'),
        project_id=graphene.ID(description='Идентификатор проекта'),
        required=True,
        description='Дивизионы пользователя'
    )
    divisions = graphene.List(
        DivisionModelType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        description='Дивизионы'
    )

    @staticmethod
    @permission_classes((IsAuthenticated, ViewProject))
    def resolve_project(root: Any, info: ResolveInfo, project_id: str) -> Project:
        return get_object_or_404(Project, pk=from_global_id(project_id)[1])

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_projects(root: Any, info: ResolveInfo, *args, **kwargs) -> QuerySet[Project]:
        return get_user_projects(info.context.user)

    @staticmethod
    @permission_classes((IsAuthenticated, ViewPeriod))
    def resolve_period(root: Any, info: ResolveInfo, period_id: str) -> Period:
        return get_object_or_404(Period, pk=from_global_id(period_id)[1])

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_periods(root: Any, info: ResolveInfo, project_id: str) -> QuerySet[Period]:
        return get_user_periods(info.context.user, from_global_id(project_id)[1])

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_user_divisions(
        root: Any,
        info: ResolveInfo,
        user_id: str | None = None,
        project_id: str | None = None,
    ) -> list[dict[str, int | str]]:
        user: User = info.context.user if user_id is None else get_object_or_404(User, pk=from_global_id(user_id)[1])
        return get_user_divisions(user, project_id)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_divisions(root: Any, info: ResolveInfo, period_id: int) -> QuerySet[Department | Organization]:
        period = get_object_or_404(Period, pk=period_id)
        return period.project.DIVISION_KIND[str(period.project.content_type.model)].objects.all()
