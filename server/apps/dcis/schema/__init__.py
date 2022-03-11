import graphene

from apps.dcis.schema.queries import DocumentQueries, PrivilegeQueries, ProjectQueries, SheetQueries
from apps.dcis.schema.mutations import DocumentMutations


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
    DocumentMutations,
    graphene.ObjectType,
):
    """Мутации приложения dcis."""

    pass
