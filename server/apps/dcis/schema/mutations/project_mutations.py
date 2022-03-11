import graphene
from graphene_django_cud.mutations import DjangoCreateMutation, DjangoDeleteMutation

from apps.dcis.models import Project, Period
from apps.dcis.schema.types import ProjectType, PeriodType


class CreateProjectMutation(DjangoCreateMutation):
    """Мутация для создания проекта."""

    class Meta:
        model = Project

    project = graphene.Field(ProjectType, description='Добавленный проект')


class DeleteProjectMutation(DjangoDeleteMutation):
    """Мутация для удаления проекта."""

    class Meta:
        model = Project


class CreatePeriodMutation(DjangoCreateMutation):
    """Мутация для создания периода."""

    class Meta:
        model = Period

    period = graphene.Field(PeriodType, description='Добавленный период')


class ProjectMutations(graphene.ObjectType):
    create_project = CreateProjectMutation.Field(required=True)
    delete_project = DeleteProjectMutation.Field(required=True)
    create_period = CreatePeriodMutation.Field(required=True)
