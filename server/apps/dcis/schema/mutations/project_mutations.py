from typing import Any

import graphene
from devind_core.models import File
from devind_dictionaries.models import Department
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphene_django_cud.mutations import DjangoCreateMutation, DjangoUpdateMutation, DjangoDeleteMutation
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.helpers import DjangoCudBaseMutation
from apps.dcis.models import Project, Period
from apps.dcis.permissions import AddPeriod
from apps.dcis.schema.types import ProjectType, PeriodType
from apps.dcis.services.excel_extractor import ExcelExtractor
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
        permissions = ('dcis.change_project',)

    project = graphene.Field(ProjectType, description='Измененный проект')


class DeleteProjectMutationPayload(DjangoCudBaseMutation, DjangoDeleteMutation):
    """Мутация на удаление проекта."""

    class Meta:
        model = Project
        login_required = True
        permissions = ('dcis.delete_project',)


class AddPeriodMutation(BaseMutation):
    """Мутация для создания периода."""

    class Input:
        name = graphene.String(required=True, description='Название периода')
        project_id = graphene.ID(required=True, description='Идентификатор проекта')
        file = Upload(required=True, description='Xlsx файл с проектом')

    period = graphene.Field(PeriodType, description='Добавленный период')

    @staticmethod
    @permission_classes((IsAuthenticated, AddPeriod,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, name: str, project_id: str, file: InMemoryUploadedFile):
        project = get_object_or_404(Project, pk=from_global_id(project_id)[1])
        period: Period = Period.objects.create(
            name=name,
            user=info.context.user,
            project=project
        )
        fl: File = period.methodical_support.create(
            name=file.name,
            src=file,
            deleted=False,
            user=info.context.user
        )
        extractor: ExcelExtractor = ExcelExtractor(fl.src.path)
        extractor.save(period)
        return AddPeriodMutation(period=period)


class ChangePeriodMutationPayload(DjangoCudBaseMutation, DjangoUpdateMutation):
    """Мутация на изменение настроек периода."""

    class Meta:
        model = Period
        login_required = True
        exclude_fields = ('project', 'methodical_support',)
        optional_fields = ('start', 'expiration', 'user',)
        permissions = ('dcis.change_period',)

    period = graphene.Field(PeriodType, description='Измененный период')


class DeletePeriodMutationPayload(DjangoCudBaseMutation, DjangoDeleteMutation):
    """Мутация на удаление периода."""

    class Meta:
        model = Period
        login_required = True
        permissions = ('dcis.delete_period',)


class ProjectMutations(graphene.ObjectType):
    """Список мутация проекта."""

    add_project = AddProjectMutationPayload.Field(required=True)
    change_project = ChangeProjectMutationPayload.Field(required=True)
    delete_project = DeleteProjectMutationPayload.Field(required=True)
    add_period = AddPeriodMutation.Field(required=True)
    change_period = ChangePeriodMutationPayload.Field(required=True)
    delete_period = DeletePeriodMutationPayload.Field(required=True)
