from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from django.db.models import QuerySet
from graphene_django_filter import AdvancedDjangoFilterConnectionField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import Project
from apps.dcis.permissions import ViewProject
from apps.dcis.schema.types import ProjectType
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
