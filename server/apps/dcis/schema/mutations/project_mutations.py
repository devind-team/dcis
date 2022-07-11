from typing import Any

import graphene
from devind_dictionaries.models import Department
from devind_helpers.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from graphene_django_cud.mutations import DjangoCreateMutation, DjangoDeleteMutation, DjangoUpdateMutation
from graphql import ResolveInfo

from apps.dcis.helpers import DjangoCudBaseMutation
from apps.dcis.models import Project
from apps.dcis.permissions import ChangeProject, DeleteProject
from apps.dcis.schema.types import ProjectType
from apps.dcis.validators import ProjectValidator


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


class ChangeProjectMutationPayload(DjangoCudBaseMutation, DjangoUpdateMutation):
    """Мутация изменения настроек проекта."""

    class Meta:
        model = Project
        login_required = True
        exclude_fields = ('content_type', 'object_id',)

    project = graphene.Field(ProjectType, description='Измененный проект')

    @classmethod
    def check_permissions(cls, root: Any, info: ResolveInfo, input: Any, id: str, obj: Project) -> None:
        if not ChangeProject.has_object_permission(info.context, obj):
            raise PermissionDenied('Ошибка доступа')


class DeleteProjectMutationPayload(DjangoCudBaseMutation, DjangoDeleteMutation):
    """Мутация на удаление проекта."""

    class Meta:
        model = Project
        login_required = True

    @classmethod
    def check_permissions(cls, root: Any, info: ResolveInfo, id: str, obj: Project) -> None:
        if not DeleteProject.has_object_permission(info.context, obj):
            raise PermissionDenied('Ошибка доступа')


class ProjectMutations(graphene.ObjectType):
    """Список мутация проекта."""

    add_project = AddProjectMutationPayload.Field(required=True)
    change_project = ChangeProjectMutationPayload.Field(required=True)
    delete_project = DeleteProjectMutationPayload.Field(required=True)
