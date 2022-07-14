"""Модуль содержит мутации, относящиеся к ячейкам."""

from typing import Any

import graphene
from devind_dictionaries.models import BudgetClassification
from devind_dictionaries.schema.types import BudgetClassificationType
from devind_helpers.decorators import permission_classes
from devind_helpers.exceptions import PermissionDenied
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.schema.types import ErrorFieldType
from graphene_django_cud.mutations import DjangoCreateMutation
from graphql import ResolveInfo
from stringcase import snakecase

from apps.dcis.models import Cell
from apps.dcis.permissions import ChangePeriodSheet
from apps.dcis.schema.types import ChangedCellOption
from apps.dcis.services.sheet_services import (
    CheckCellOptions,
    change_cells_option,
)


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
            'n', 's', 'f', 'b', 'inlineStr', 'e', 'str', 'd', 'text', 'money',
            'bigMoney', 'fl', 'user', 'department', 'organization', 'classification'
        ]
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
    @permission_classes((IsAuthenticated, ChangePeriodSheet,))
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
                if len(set(cells.values_list('row__sheet__period', flat=True))) != 1:
                    raise PermissionDenied('Ошибка доступа')
                info.context.check_object_permissions(info.context, cells.first().row.sheet.period)
                return ChangeCellsOptionMutation(changed_options=change_cells_option(cells, field, value))


class AddBudgetClassificationMutationPayload(DjangoCreateMutation):
    """Мутация для добавления КБК в словарь."""

    class Meta:
        model = BudgetClassification
        login_required = True
        required_fields = ('code', 'name',)
        permissions = ('devind_dictionaries.add_budgetclassification',) # noqa

    budget_classification = graphene.Field(BudgetClassificationType, description='Добавленная КБК')


class CellMutations(graphene.ObjectType):
    """Мутации, связанные с ячейками."""

    change_cells_option = ChangeCellsOptionMutation.Field(required=True, description='Изменения опций ячейки')
    add_budget_classification = AddBudgetClassificationMutationPayload.Field(
        required=True,
        description='Добавление нового КБК'
    )
