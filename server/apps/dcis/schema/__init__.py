import graphene

from apps.dcis.schema.queries import DocumentQueries, PrivilegeQueries, ProjectQueries, SheetQueries
from apps.dcis.schema.mutations import DocumentMutations, ProjectMutations


class Query(
    DocumentQueries,
    PrivilegeQueries,
    ProjectQueries,
    SheetQueries,
    graphene.ObjectType,
):
    """Запросы приложения dcis."""

    pass


class Mutation(
    ProjectMutations,
    DocumentMutations,
    graphene.ObjectType,
):
    """Мутации приложения dcis."""

    pass
