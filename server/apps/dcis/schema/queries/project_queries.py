from typing import Any, Optional

import graphene
from devind_dictionaries.models import Department, Organization
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from graphene_django import DjangoListField
from graphene_django_filter import AdvancedDjangoFilterConnectionField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.models import User
from apps.dcis.models import Project, Period
from ..types import DivisionType, DivisionModelType, ProjectType, PeriodType, DivisionUnionType


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
        user_id=graphene.ID(required=True, description='Идентификатор пользователя'),
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
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
        DivisionUnionType,
        period_id=graphene.ID(required=True, description='Идентификатор пeриода'),
        description='Дивизионы'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def resolve_periods(root: Any, info: ResolveInfo, user_id: str, period_id: str, *args, **kwargs):
        return Period.objects.filter(periodprivilege__user=from_global_id(user_id)[1]).exclude(pk=period_id).all()

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
    def resolve_user_divisions(
            root: Any,
            info: ResolveInfo,
            user_id: Optional[str] = None,
            project_id: Optional[str] = None
    ) -> list:
        user: User = info.context.user \
            if user_id is None \
            else get_object_or_404(User, pk=from_global_id(user_id)[1])
        project: Optional[Project] = None \
            if project_id is None \
            else get_object_or_404(Project, pk=from_global_id(project_id)[1])
        divisions = user.divisions(project)
        return divisions

    @staticmethod
    def resolve_divisions(root: Any, info: ResolveInfo, period_id: int, *args, **kwargs):
        divisions = []
        period = get_object_or_404(Period, pk=period_id)
        if ContentType.objects.get_for_id(period.project.content_type_id).model == 'department':
            departments = Department.objects.all()
            divisions.extend(departments)
        else:
            organizations = Organization.objects.all()
            divisions.extend(organizations)
        return divisions
