import graphene

from apps.dcis.schema.mutations import (
    CellMutations,
    DocumentMutations,
    ProjectMutations,
    PeriodMutations,
    SheetMutations,
    ValueMutations,
    AttributeMutations,
)
from apps.dcis.schema.queries import DocumentQueries, PeriodQueries, ProjectQueries


class Query(
    DocumentQueries,
    PeriodQueries,
    ProjectQueries,
    graphene.ObjectType,
):
    """Запросы приложения dcis."""

    ...


class Mutation(
    CellMutations,
    DocumentMutations,
    PeriodMutations,
    ProjectMutations,
    SheetMutations,
    ValueMutations,
    AttributeMutations,
    graphene.ObjectType,
):
    """Мутации приложения dcis."""

    ...
