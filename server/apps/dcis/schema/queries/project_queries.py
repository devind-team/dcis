import graphene
from graphene_django_filter import AdvancedDjangoFilterConnectionField

from ..types import ProjectType


class ProjectQueries(graphene.ObjectType):
    """Запросы записей, связанных с проектами."""

    projects = AdvancedDjangoFilterConnectionField(ProjectType)
