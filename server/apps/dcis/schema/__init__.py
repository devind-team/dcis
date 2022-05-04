import graphene

from apps.dcis.schema.queries import DocumentQueries, PrivilegeQueries, ProjectQueries, SheetQueries
from apps.dcis.schema.mutations import CellMutations, DocumentMutations, ProjectMutations, SheetMutations


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
    CellMutations,
    ProjectMutations,
    DocumentMutations,
    SheetMutations,
    graphene.ObjectType,
):
    """Мутации приложения dcis."""

    pass
