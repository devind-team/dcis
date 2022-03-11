import graphene

from apps.dcis.schema.queries import DocumentQueries, PrivilegeQueries, ProjectQueries, SheetQueries
from apps.dcis.schema.mutations import ProjectMutations


class Query(
    DocumentQueries,
    PrivilegeQueries,
    ProjectQueries,
    SheetQueries,
    graphene.ObjectType
):
    """Запросы приложения dcis."""

    pass


class Mutation(
    ProjectMutations,
    graphene.ObjectType
):
    """Мутации приложения dcis."""

    pass
