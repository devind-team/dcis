import graphene

from apps.dcis.schema.types import ProjectType
from apps.dcis.schema.mutations import ProjectMutations


class Mutation(
    ProjectMutations,
    graphene.ObjectType
):
    """Мутации приложения dcis."""

    pass
