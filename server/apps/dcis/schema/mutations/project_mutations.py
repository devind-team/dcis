from typing import Any

import graphene
from devind_dictionaries.models import Department
from devind_helpers.exceptions import PermissionDenied
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.decorators import permission_classes
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.schema.types import ErrorFieldType
from django.contrib.contenttypes.models import ContentType
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.helpers import DjangoCudBaseMutation
from apps.dcis.models import Project
from apps.dcis.permissions import AddProject, ChangeProject, DeleteProject
from apps.dcis.schema.types import ProjectType
from apps.dcis.validators import ProjectValidator
from apps.dcis.services.project_services import (
    create_project,
    change_project,
    delete_project
)


class AddProjectMutation(BaseMutation):
    """Мутация для добавления проекта."""

    class Input:
        name = graphene.String(required=True, description='Наименование проекта')
        short = graphene.String(required=True, description='Сокращенное наименование проекта')
        description = graphene.String(required=True, description='Описание проекта')
        visibility = graphene.Boolean(description='Видимость проекта')
        content_type = graphene.String(required=True, description='Тип дивизиона')

    project = graphene.Field(ProjectType, description='Добавленный проект')

    @staticmethod
    @permission_classes((IsAuthenticated, AddProject,))
    def mutate_and_get_payload(
            root: Any,
            info: ResolveInfo,
            visibility: bool,
            **kwargs
    ):
        validator = ProjectValidator(kwargs)
        if not validator.validate():
            return AddProjectMutation(success=False, error=ErrorFieldType.from_validator(validator.get_message()))
        kwargs.values()
        return AddProjectMutation(project=create_project(kwargs, visibility))


class ChangeProjectMutation(BaseMutation):
    """Мутация изменения настроек проекта."""

    class Input:
        project_id = graphene.ID(required=True, description='Идентификатор проекта')
        name = graphene.String(description='Наименование проекта')
        short = graphene.String(description='Сокращенное наименование проекта')
        description = graphene.String(description='Описание проекта')
        visibility = graphene.Boolean(description='Видимость проекта')
        archive = graphene.Boolean(description='Архив')

    project = graphene.Field(ProjectType, description='Измененный проект')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangeProject,))
    def mutate_and_get_payload(
            root: Any,
            info: ResolveInfo,
            project_id: str | int,
            name: str,
            short: str,
            description: str,
            visibility: bool,
            archive: bool
    ):
        project: Project = get_object_or_404(Project, pk=from_global_id(project_id)[1])
        info.context.check_object_permissions(info.context, project)
        return ChangeProjectMutation(project=change_project(project, name, short, description, visibility, archive))


class DeleteProjectMutation(BaseMutation):
    """Мутация на удаление проекта."""

    class Input:
        project_id = graphene.ID(required=True, description='Идентификатор проекта')

    delete_id = graphene.ID(required=True, description='Идентификатор удаленного проекта')

    @staticmethod
    @permission_classes((IsAuthenticated, DeleteProject,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, project_id: str | int):
        project: Project = get_object_or_404(Project, pk=from_global_id(project_id)[1])
        info.context.check_object_permissions(info.context, project)
        delete_project(project)
        return DeleteProjectMutation(delete_id=project_id)


class ProjectMutations(graphene.ObjectType):
    """Список мутация проекта."""

    add_project = AddProjectMutation.Field(required=True)
    change_project = ChangeProjectMutation.Field(required=True)
    delete_project = DeleteProjectMutation.Field(required=True)
