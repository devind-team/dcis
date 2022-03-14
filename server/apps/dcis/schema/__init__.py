import graphene

from apps.dcis.schema.queries import DocumentQueries, PrivilegeQueries, ProjectQueries, SheetQueries
from apps.dcis.schema.mutations import DocumentMutations, ProjectMutations, SheetMutations


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
    SheetMutations,
    graphene.ObjectType,
):
    """Мутации приложения dcis."""

    pass
