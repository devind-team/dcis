import graphene
from graphene_django_cud.mutations import DjangoCreateMutation, DjangoDeleteMutation

from apps.dcis.models import Project
from apps.dcis.schema.types import ProjectType


class CreateProjectMutation(DjangoCreateMutation):
    """Мутация для создания проекта."""

    class Meta:
        model = Project

    project = graphene.Field(ProjectType, description='Добавленный проект')


class DeleteProjectMutation(DjangoDeleteMutation):
    """Мутация для удаления проекта."""

    class Meta:
        model = Project


class ProjectMutations(graphene.ObjectType):
    create_project = CreateProjectMutation.Field(required=True)
    delete_project = DeleteProjectMutation.Field(required=True)
