"""Модуль содержит мутации, относящиеся к ячейкам."""

from typing import Any

import graphene
from devind_dictionaries.schema.types import BudgetClassificationType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.schema.types import ErrorFieldType
from devind_helpers.utils import gid2int
from graphql import ResolveInfo
from stringcase import snakecase

from apps.dcis.models import Cell
from apps.dcis.schema.types import (
    CellPasteOptionsInputType,
    CellPasteOptionsType,
    ChangeCellType,
    ChangedCellOptionType,
)
from apps.dcis.services.aggregation_services import add_cell_aggregation, delete_cell_aggregation
from apps.dcis.services.sheet_services import (
    CellPasteOptions,
    CellPasteStyle,
    CheckCellOptions,
    add_budget_classification,
    change_cell_default,
    change_cells_option,
    check_cells_permissions,
    paste_into_cells,
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
        cell: Cell = get_object_or_404(Cell, pk=gid2int(cell_id))
        change_cell_default(user=info.context.user, cell=cell, default=default)
        return ChangeCellDefault(cell_id=cell.id, default=cell.default)


class ChangeCellsOptionMutation(BaseMutation):
    """Изменение свойств ячеек:

        - strong - true, false
        - italic - true, false
        - underline - [None, 'single', 'double', 'single_accounting', 'double_accounting']
        - strike - true, false
        - horizontal_align - ['left', 'center', 'right']
        - vertical_align - ['top', 'middle', 'bottom']
        - size - число от 6 до 24
        - kind - [
            'n', 's', 'f', 'b', 'inlineStr', 'e', 'str', 'd', 'time', 'text', 'money',
            'bigMoney', 'fl', 'user', 'department', 'organization', 'classification'
        ]
        - number_format - форматирование чисел
        - aggregation - [None, 'sum', 'avg', 'min', 'max']
    """

    class Input:
        cell_ids = graphene.List(graphene.NonNull(graphene.ID), required=True, description='Идентификаторы ячеек')
        field = graphene.String(required=True, description='Идентификатор поля')
        value = graphene.String(description='Значение поля')

    changed_options = graphene.List(
        graphene.NonNull(ChangedCellOptionType),
        description='Измененные свойства ячеек'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        cell_ids: list[str],
        field: str,
        value: str | None = None
    ):
        field = snakecase(field)
        match CheckCellOptions(field, value):
            case CheckCellOptions.Error(field, error):
                return ChangeCellsOptionMutation(success=False, errors=[ErrorFieldType(field, [error])])
            case CheckCellOptions.Success(value):
                cells = Cell.objects.filter(pk__in=map(gid2int, cell_ids))
                check_cells_permissions(user=info.context.user, cells=cells)
                return ChangeCellsOptionMutation(changed_options=change_cells_option(cells, field, value))


class PasteIntoCellsMutation(BaseMutation):
    """Вставка в ячейки."""

    class Input:
        options = graphene.List(
            graphene.NonNull(CellPasteOptionsInputType),
            required=True,
            description='Данные для вставки в ячейки'
        )

    changed_options = graphene.List(
        graphene.NonNull(CellPasteOptionsType),
        description='Результат вставки в ячейки'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, options: list[CellPasteOptionsInputType]):
        cells = Cell.objects.filter(pk__in=(gid2int(option.cell_id) for option in options))
        check_cells_permissions(user=info.context.user, cells=cells)
        past_options: list[CellPasteOptions] = []
        for option in options:
            if option.style:
                for field in ['horizontal_align', 'vertical_align', 'underline', 'size']:
                    match CheckCellOptions(field, getattr(option.style, field)):
                        case CheckCellOptions.Error(field, error):
                            return PasteIntoCellsMutation(success=False, errors=[ErrorFieldType(field, [error])])
            cell = next(cell for cell in cells if cell.id == gid2int(option.cell_id))
            past_options.append(CellPasteOptions(
                cell=cell,
                default=option.default,
                style=CellPasteStyle(
                    strong=option.style.strong,
                    italic=option.style.italic,
                    underline=option.style.underline,
                    strike=option.style.strike,
                    horizontal_align=option.style.horizontal_align,
                    vertical_align=option.style.vertical_align,
                    size=option.style.size,
                    color=option.style.color,
                    background=option.style.background,
                ) if option.style else None
            ))
        return PasteIntoCellsMutation(changed_options=paste_into_cells(past_options))


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
        return AddBudgetClassificationMutation(
            budget_classification=add_budget_classification(
                info.context.user,
                code,
                name,
            )
        )


class AddValuesCellsMutation(BaseMutation):
    """Добавление связной ячейки к агрегирующей."""

    class Input:
        cell_id = graphene.ID(required=True, description='Целевая ячейка')
        cells_id = graphene.List(
            graphene.NonNull(graphene.ID, required=True, description='Идентификаторы ячеек'),
            required=True,
            description='Связываем ячейки'
        )

    cells = graphene.List(ChangeCellType, description='Добавленные ячейки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        cell_id: str,
        cells_id: list[str]
    ) -> 'AddValuesCellsMutation':
        cells, errors = add_cell_aggregation(info.context.user, cell_id, cells_id)
        return AddValuesCellsMutation(success=not errors, errors=errors, cells=cells)


class DeleteValuesCellMutation(BaseMutation):
    """Удаление агрегирующий ячейки."""

    class Input:
        cell_id = graphene.ID(required=True, description='Агрегирующая ячейка')
        target_cell_id = graphene.ID(required=True, description='Целевая ячейка')

    id = graphene.ID(description='Идентификатор удаленной ячейки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        cell_id: str,
        target_cell_id: str
    ) -> 'DeleteValuesCellMutation':
        return DeleteValuesCellMutation(id=delete_cell_aggregation(info.context.user, cell_id, target_cell_id))


class CellMutations(graphene.ObjectType):
    """Мутации, связанные с ячейками."""

    change_cell_default = ChangeCellDefault.Field(required=True, description='Изменение значения ячейки по умолчанию')
    change_cells_option = ChangeCellsOptionMutation.Field(required=True, description='Изменения опций ячейки')
    paste_into_cells = PasteIntoCellsMutation.Field(required=True, description='Вставка в ячейки')
    add_budget_classification = AddBudgetClassificationMutation.Field(
        required=True,
        description='Добавление нового КБК'
    )

    add_values_cells = AddValuesCellsMutation.Field(required=True, description='Добавляем агрегирование ячейки')
    delete_values_cell = DeleteValuesCellMutation.Field(required=True, description='Удаление агрегированной ячейки')
