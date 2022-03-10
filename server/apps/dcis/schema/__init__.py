import graphene

from apps.dcis.schema.queries import DocumentQueries, PrivilegeQueries, ProjectQueries, SheetQueries


class Query(
    DocumentQueries,
    PrivilegeQueries,
    ProjectQueries,
    SheetQueries,
    graphene.ObjectType
):
    """Запросы приложения dcis."""

    pass


class Mutation(graphene.ObjectType):
    """Мутации приложения dcis."""

    pass
