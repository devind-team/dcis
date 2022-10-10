"""Модуль содержит мутации, относящиеся к ячейкам."""

from typing import Any

import graphene
from devind_dictionaries.schema.types import BudgetClassificationType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.schema.types import ErrorFieldType
from graphql import ResolveInfo
from stringcase import snakecase

from apps.dcis.models import Cell
from apps.dcis.schema.types import ChangedCellOption
from apps.dcis.services.sheet_services import (
    CheckCellOptions,
    change_cell_default,
    success_check_cell_options,
    change_cells_option,
    add_budget_classification
)


class ChangeCellDefault(BaseMutation):
    """Изменение значения ячейки по умолчанию."""

    class Input:
        cell_id = graphene.ID(required=True, description='Идентификатор ячейки')
        default = graphene.String(required=True, description='Значение по умолчанию')

    cell_id = graphene.ID(required=True, description='Идентификатор ячейки')
    default = graphene.String(required=True, description='Значение по умолчанию')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, cell_id: str, default: str):
        cell: Cell = get_object_or_404(Cell, pk=cell_id)
        change_cell_default(user=info.context.user, cell=cell, default=default)
        return ChangeCellDefault(cell_id=cell.id, default=cell.default)


class ChangeCellsOptionMutation(BaseMutation):
    """Изменение свойств ячеек:

        - strong - true, false
        - italic - true, false
        - strike - true, false
        - underline - [None, 'single', 'double', 'single_accounting', 'double_accounting']
        - horizontal_align - ['left', 'center', 'right']
        - vertical_align - ['top', 'middle', 'bottom']
        - size - число от 6 до 24
        - kind - [
            'n', 's', 'f', 'b', 'inlineStr', 'e', 'str', 'd', 'time', 'text', 'money',
            'bigMoney', 'fl', 'user', 'department', 'organization', 'classification'
        ]
        - number_format - форматирование чисел
    """

    class Input:
        cell_ids = graphene.List(graphene.NonNull(graphene.ID), required=True, description='Идентификаторы ячеек')
        field = graphene.String(required=True, description='Идентификатор поля')
        value = graphene.String(description='Значение поля')

    changed_options = graphene.List(
        graphene.NonNull(ChangedCellOption),
        description='Измененные свойства ячеек'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        cell_ids: list[int],
        field: str,
        value: str | None = None
    ):
        field = snakecase(field)
        match CheckCellOptions(field, value):
            case CheckCellOptions.Error(field, error):
                return ChangeCellsOptionMutation(success=False, errors=[ErrorFieldType(field, [error])])
            case CheckCellOptions.Success(value):
                cells = Cell.objects.filter(pk__in=cell_ids).all()
                success_check_cell_options(user=info.context.user, cells=cells)
                return ChangeCellsOptionMutation(changed_options=change_cells_option(cells, field, value))


class AddBudgetClassificationMutation(BaseMutation):
    """Мутация для добавления КБК в словарь."""

    class Input:
        code = graphene.String(required=True, description='Code')
        name = graphene.String(required=True, description='Name')

    budget_classification = graphene.Field(BudgetClassificationType, description='Добавленная КБК')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        code: str,
        name: str
    ):
        return AddBudgetClassificationMutation(budget_classification=add_budget_classification(
            info.context.user,
            code,
            name)
        )


class CellMutations(graphene.ObjectType):
    """Мутации, связанные с ячейками."""

    change_cell_default = ChangeCellDefault.Field(required=True, description='Изменение значения ячейки по умолчанию')
    change_cells_option = ChangeCellsOptionMutation.Field(required=True, description='Изменения опций ячейки')
    add_budget_classification = AddBudgetClassificationMutation.Field(
        required=True,
        description='Добавление нового КБК'
    )
