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
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Периоды'
    )
    period = graphene.Field(
        PeriodType,
        period_id=graphene.ID(required=True, description='Идентификатор периода'),
        required=True,
        description='Информация по периоду'
    )

    period_divisions = AdvancedDjangoFilterConnectionField(DivisionType, description='Получение дивизионов')
    user_divisions = graphene.List(
        DivisionModelType,
        user_id=graphene.ID(description='Пользователь'),
        project_id=graphene.ID(description='Идентификатор проекта'),
        required=True,
        description='Дивизионы пользователя'
    )
    divisions = graphene.List(
        DivisionUnionType,
        project_id=graphene.ID(required=True, description='Идентификатор проекта'),
        search_text=graphene.String(description='Название дивизиона'),
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
    def resolve_divisions(root: Any, info: ResolveInfo, project_id: int, search_text: str, *args, **kwargs):
        items = []
        project = get_object_or_404(Project, pk=project_id)
        if ContentType.objects.get_for_id(project.content_type_id).model == 'department':
            departments = Department.objects.filter(name__contains=search_text)
            items.extend(departments)
        else:
            organizations = Organization.objects.filter(name__contains=search_text)
            items.extend(organizations)
        return items
