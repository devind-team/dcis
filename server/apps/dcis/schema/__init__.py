import graphene

from apps.dcis.schema.mutations import (
    CellMutations,
    DocumentMutations,
    PrivilegeMutations,
    ProjectMutations,
    SheetMutations,
    ValueMutations,
)
from apps.dcis.schema.queries import DocumentQueries, PrivilegeQueries, ProjectQueries, SheetQueries


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
    PrivilegeMutations,
    ValueMutations,
    graphene.ObjectType,
):
    """Мутации приложения dcis."""

    pass
