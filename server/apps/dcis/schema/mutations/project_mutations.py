from typing import Any

import graphene
from graphql import ResolveInfo
from graphene_file_upload.scalars import Upload
from devind_helpers.schema.mutations import BaseMutation
from django.core.files.uploadedfile import InMemoryUploadedFile
from devind_helpers.decorators import permission_classes
from devind_helpers.permissions import IsAuthenticated
from graphql_relay import from_global_id
from devind_helpers.orm_utils import get_object_or_404
from devind_core.models import File

from apps.dcis.models import Project, Period
from apps.dcis.schema.types import ProjectType, PeriodType
from apps.dcis.services.excel_extractor import ExcelExtractor


class AddProjectMutation(BaseMutation):
    """Мутация для добавления проекта."""

    class Input:
        name = graphene.String(required=True, description='Название проекта')
        short = graphene.String(required=True, description='Название проекта')
        description = graphene.String(required=True, description='Описание проекта')

    project = graphene.Field(ProjectType, description='Добавленный проект')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, name: str, short: str, description: str, *args, **kwargs):
        project: Project = Project.objects.create(
            name=name,
            short=short,
            description=description,
            user=info.context.user
        )
        return AddProjectMutation(project=project)


class AddPeriodMutation(BaseMutation):
    """Мутация для создания периода."""

    class Input:
        name = graphene.String(required=True, description='Название периода')
        project_id = graphene.ID(required=True, description='Идентификатор проекта')
        file = Upload(required=True, description='Xlsx файл с проектом')

    period = graphene.Field(PeriodType, description='Добавленный период')

    @staticmethod
    @permission_classes((IsAuthenticated,))
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


class ProjectMutations(graphene.ObjectType):
    """Список мутация проекта."""
    add_project = AddProjectMutation.Field(required=True)
    add_period = AddPeriodMutation.Field(required=True)
