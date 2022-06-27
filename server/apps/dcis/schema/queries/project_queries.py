from typing import Any, Optional

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from graphene_django import DjangoListField
from graphene_django_filter import AdvancedDjangoFilterConnectionField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.models import User
from apps.dcis.models import Period, Project
from ..types import DivisionModelType, PeriodType, ProjectType
from ...services.divisions_services import get_user_divisions
from ...services.period_services import get_user_periods
from ...services.project_services import get_user_projects


class ProjectQueries(graphene.ObjectType):
    """Запросы записей, связанных с проектами."""

    project = graphene.Field(
        ProjectType,
        project_id=graphene.ID(required=True, description='Идентификатор проекта'),
        required=True,
        description='Получение информации по проекту'
    )
    projects = AdvancedDjangoFilterConnectionField(ProjectType)

    period = graphene.Field(
        PeriodType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Информация по периоду'
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
    @permission_classes((IsAuthenticated,))
    def resolve_project(root: Any, info: ResolveInfo, project_id: str, *args, **kwargs):
        return get_object_or_404(Project, pk=from_global_id(project_id)[1])

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_projects(root: Any, info: ResolveInfo, *args, **kwargs):
        return get_user_projects(info.context.user)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_period(root: Any, info: ResolveInfo, period_id: str, *args, **kwargs):
        return get_object_or_404(Period, pk=from_global_id(period_id)[1])

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_periods(root: Any, info: ResolveInfo, project_id: str, *args, **kwargs):
        return get_user_periods(info.context.user, from_global_id(project_id)[1])

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_user_divisions(
            root: Any,
            info: ResolveInfo,
            user_id: Optional[str] = None,
            project_id: Optional[str] = None
    ) -> list:
        user: User = info.context.user if user_id is None else get_object_or_404(User, pk=from_global_id(user_id)[1])
        return get_user_divisions(user, project_id)

    @staticmethod
    def resolve_divisions(root: Any, info: ResolveInfo, period_id: int, *args, **kwargs):
        period = get_object_or_404(Period, pk=period_id)
        return period.project.DIVISION_KIND[str(period.project.content_type.model)].objects.all()
