import graphene

from apps.dcis.schema.mutations import (
    AttributeMutations,
    CellMutations,
    CuratorMutations,
    DocumentMutations,
    PeriodMutations,
    ProjectMutations,
    SheetMutations,
    ValueMutations,
)
from apps.dcis.schema.queries import DocumentQueries, PeriodQueries, ProjectQueries, CuratorGroupQueries


class Query(
    DocumentQueries,
    PeriodQueries,
    ProjectQueries,
    CuratorGroupQueries,
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
    CuratorMutations,
    graphene.ObjectType
):
    """Мутации приложения dcis."""

    ...
