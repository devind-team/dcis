import graphene

from apps.dcis.schema.mutations import (
    AttributeMutations,
    CellMutations,
    CuratorMutations,
    DocumentMutations,
    LimitationMutations,
    PeriodMutations,
    ProjectMutations,
    SheetMutations,
    ValueMutations,
)
from apps.dcis.schema.queries import CuratorGroupQueries, DocumentQueries, PeriodQueries, ProjectQueries


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
    LimitationMutations,
    graphene.ObjectType
):
    """Мутации приложения dcis."""

    ...
