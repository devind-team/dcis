from typing import Any

import graphene
from devind_dictionaries.models import Department
from devind_helpers.exceptions import PermissionDenied
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.decorators import permission_classes
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.orm_utils import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from graphene_django_cud.mutations import DjangoCreateMutation, DjangoDeleteMutation, DjangoUpdateMutation
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.helpers import DjangoCudBaseMutation
from apps.dcis.models import Project
from apps.dcis.permissions import ChangeProject, DeleteProject
from apps.dcis.schema.types import ProjectType
from apps.dcis.validators import ProjectValidator
from apps.dcis.services.project_services import (
    change_project,
    delete_project
)


class AddProjectMutationPayload(DjangoCudBaseMutation, DjangoCreateMutation):
    """Мутация для добавления проекта."""

    class Meta:
        model = Project
        login_required = True
        field_types = {
            'content_type': graphene.String(required=True)
        }
        permissions = ('dcis.add_project',)
        auto_context_fields = {'user': 'user'}

    project = graphene.Field(ProjectType, description='Добавленный проект')

    @classmethod
    def validate(cls, root: Any, info: ResolveInfo, input, *args, **kwargs):
        validator: ProjectValidator = ProjectValidator(input)
        if validator.validate():
            super().validate(root, info, input)
        else:
            raise ValueError(validator.validate_message_plain)

    @classmethod
    def handle_content_type(cls, value: str, field: str, info: ResolveInfo, *args, **kwargs):
        return ContentType.objects.get_for_model(Project.DIVISION_KIND.get(value, Department))


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

    add_project = AddProjectMutationPayload.Field(required=True)
    change_project = ChangeProjectMutation.Field(required=True)
    delete_project = DeleteProjectMutation.Field(required=True)
