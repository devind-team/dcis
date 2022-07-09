import graphene

from apps.dcis.schema.mutations import (
    CellMutations,
    DocumentMutations,
    PrivilegeMutations,
    ProjectMutations,
    PeriodMutations,
    SheetMutations,
)
from apps.dcis.schema.queries import DocumentQueries, PeriodQueries, ProjectQueries


class Query(
    DocumentQueries,
    PeriodQueries,
    ProjectQueries,
    graphene.ObjectType,
):
    """Запросы приложения dcis."""

    pass


class Mutation(
    CellMutations,
    DocumentMutations,
    PeriodMutations,
    PrivilegeMutations,
    ProjectMutations,
    SheetMutations,
    graphene.ObjectType,
):
    """Мутации приложения dcis."""

    pass
