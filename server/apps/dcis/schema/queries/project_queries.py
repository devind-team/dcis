from typing import Any

import graphene
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
from apps.dcis.services.divisions_services import get_divisions, get_user_divisions
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

    project_divisions = graphene.List(
        DivisionModelType,
        project_id=graphene.ID(required=True, description='Идентификатор проекта'),
        description='Возможные дивизионы проекта'
    )

    user_divisions = graphene.List(
        DivisionModelType,
        user_id=graphene.ID(description='Пользователь'),
        project_id=graphene.ID(description='Идентификатор проекта'),
        required=True,
        description='Дивизионы пользователя'
    )

    @staticmethod
    @permission_classes((IsAuthenticated, ViewProject))
    def resolve_project(root: Any, info: ResolveInfo, project_id: str) -> Project:
        project = get_object_or_404(Project, pk=from_global_id(project_id)[1])
        info.context.check_object_permissions(info.context, project)
        return project

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_projects(root: Any, info: ResolveInfo, *args, **kwargs) -> QuerySet[Project]:
        return get_user_projects(info.context.user)

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
    @permission_classes((IsAuthenticated, ViewProject,))
    def resolve_project_divisions(root: Any, info: ResolveInfo, project_id: str) -> list[dict[str, int | str]]:
        project = get_object_or_404(Project, pk=from_global_id(project_id)[1])
        info.context.check_object_permissions(info.context, project)
        return get_divisions(project.division.objects.all())

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
