from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from graphene_django import DjangoListField
from graphene_django_filter import AdvancedDjangoFilterConnectionField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import Project, Period
from apps.core.models import User
from ..types import ProjectType, PeriodType


class ProjectQueries(graphene.ObjectType):
    """Запросы записей, связанных с проектами."""

    projects = AdvancedDjangoFilterConnectionField(ProjectType)
    project = graphene.Field(
        ProjectType,
        project_id=graphene.ID(required=True, description='Идентификатор проекта'),
        required=True,
        description='Получение информации по проекту'
    )
    periods = DjangoListField(
        PeriodType,
        user_id=graphene.ID(required=True, description='Идентификатор пользователя'),
        required=True,
        description='Периоды'
    )
    period = graphene.Field(
        PeriodType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Информация по периоду'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_project(root: Any, info: ResolveInfo, project_id: str, *args, **kwargs):
        return get_object_or_404(Project, pk=from_global_id(project_id)[1])

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_period(root: Any, info: ResolveInfo, period_id: str, *args, **kwargs):
        return get_object_or_404(Period, pk=from_global_id(period_id)[1])

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_periods(root: Any, info: ResolveInfo, user_id: str, *args, **kwargs):
        return set(Period.objects.filter(periodprivilege__user=from_global_id(user_id)[1]).all())
