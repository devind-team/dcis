from typing import Any

import graphene
from graphql import ResolveInfo
from graphene_django_filter import AdvancedDjangoFilterConnectionField
from devind_helpers.orm_utils import get_object_or_404
from graphql_relay import from_global_id
from devind_helpers.decorators import permission_classes
from devind_helpers.permissions import IsAuthenticated

from apps.dcis.models import Project, Period
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
