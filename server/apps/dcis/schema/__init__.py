import graphene

from apps.dcis.schema.mutations import (
    CellMutations,
    DocumentMutations,
    ProjectMutations,
    PeriodMutations,
    SheetMutations,
    PrivilegeMutations,
    ValueMutations
)
from apps.dcis.schema.queries import DocumentQueries, PeriodQueries, ProjectQueries


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
    DocumentMutations,
    PeriodMutations,
    ProjectMutations,
    SheetMutations,
    PrivilegeMutations,
    ValueMutations,
    graphene.ObjectType,
):
    """Мутации приложения dcis."""

    pass
