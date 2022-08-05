from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.schema.types import ErrorFieldType
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import Project
from apps.dcis.schema.types import ProjectType
from apps.dcis.services.project_services import (change_project, create_project, delete_project)
from apps.dcis.validators import ProjectValidator


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
    @permission_classes((IsAuthenticated,))
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
        return AddProjectMutation(project=create_project(info.context.user, kwargs, visibility))


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
    @permission_classes((IsAuthenticated,))
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
        return ChangeProjectMutation(project=change_project(
            user=info.context.user,
            project=project,
            name=name,
            short=short,
            description=description,
            visibility=visibility,
            archive=archive)
        )


class DeleteProjectMutation(BaseMutation):
    """Мутация на удаление проекта."""

    class Input:
        project_id = graphene.ID(required=True, description='Идентификатор проекта')

    delete_id = graphene.ID(required=True, description='Идентификатор удаленного проекта')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, project_id: str | int):
        project: Project = get_object_or_404(Project, pk=from_global_id(project_id)[1])
        delete_project(info.context.user, project)
        return DeleteProjectMutation(delete_id=project_id)


class ProjectMutations(graphene.ObjectType):
    """Список мутация проекта."""

    add_project = AddProjectMutation.Field(required=True)
    change_project = ChangeProjectMutation.Field(required=True)
    delete_project = DeleteProjectMutation.Field(required=True)
