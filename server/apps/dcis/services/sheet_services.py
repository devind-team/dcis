import re
from argparse import ArgumentTypeError
from typing import NamedTuple, Sequence

from devind_dictionaries.models import BudgetClassification
from devind_helpers.exceptions import PermissionDenied
from devind_helpers.utils import convert_str_to_bool, convert_str_to_int
from django.db import transaction
from django.db.models import QuerySet
from stringcase import camelcase
from xlsx_evaluate.tokenizer import ExcelParser, f_token

from apps.core.models import User
from apps.dcis.models import Period, Sheet, Value
from apps.dcis.models.sheet import Cell
from apps.dcis.permissions import (
    can_add_budget_classification,
    can_change_period_sheet,
)


@transaction.atomic
def rename_sheet(user: User, sheet: Sheet, name: str) -> tuple[Sheet, list[Cell]]:
    """Переименование листа с учетом формул.

    sheet.name -> name
    :param user - пользователь
    :param sheet - лист
    :param name - новое имя листа
    """
    can_change_period_sheet(user, sheet.period)
    changed_cell: list[Cell] = []
    sheet_name: str = f"'{name}'" if ' ' in name else name
    period: Period = sheet.period
    period_sheets = period.sheet_set.exclude(pk=sheet.pk).all()
    cells: Sequence[Cell] = Cell.objects.filter(
        formula__isnull=False,
        formula__istartswith='=',
        row__parent__isnull=True,
        row__sheet__in=[sheet, *period_sheets]
    ).all()
    for cell in cells:
        tokens: list[f_token] = [
            token for token in ExcelParser().parse(cell.formula).items
            if token.tsubtype == 'range' and '!' in token.tvalue
        ]
        if not tokens:
            continue
        sheets_names: list[str] = [token.tvalue.split('!')[0] for token in tokens]
        if sheet.name in sheets_names:
            cell.formula = re.sub(f"([\'|\"]?{sheet.name}[\'|\"]?)", sheet_name, cell.formula)
            cell.save(update_fields=('formula',))
            changed_cell.append(cell)
    sheet.name = name
    sheet.save(update_fields=('name',))
    return sheet, changed_cell


class CheckCellOptions:
    """Проверка возможности изменения свойств ячеек."""

    class Success(NamedTuple):
        value: str | int | bool

    class Error(NamedTuple):
        field: str
        error: str

    def __new__(cls, field: str, value: str) -> Success | Error:
        if field not in cls._allowed_fields:
            return cls.Error('field', f'Свойство не в списке разрешенных: {field} -> {", ".join(cls._allowed_fields)}.')
        if field == 'horizontal_align':
            return cls._standard_check(field, value, cls._allowed_horizontal_align)
        if field == 'vertical_align':
            return cls._standard_check(field, value, cls._allowed_vertical_align)
        if field == 'underline':
            return cls._standard_check(field, value, cls._allowed_underline)
        if field == 'kind':
            return cls._standard_check(field, value, cls._allowed_kinds)
        if field == 'size':
            value = convert_str_to_int(value)
            if not value:
                return cls.Error('value', f'Значение свойства {field} не является числом: {value}.')
            if not (6 <= value <= 24):
                return cls.Error(
                    'value',
                    f'Значение свойства {field} не входит в разрешенный диапазон: 10 <= {value} <= 24.'
                )
            return cls.Success(value)
        if field in ['strong', 'italic', 'strike', 'editable']:
            try:
                value = convert_str_to_bool(value)
                return cls.Success(value)
            except ArgumentTypeError:
                return cls.Error(
                    'value',
                    cls._get_value_error_message(
                        field, value, ['yes', 'true', 't', 'y', '1', 'no', 'false', 'f', 'n', '0']
                    )
                )
        if field == 'number_format':
            return cls.Success(value)
        if field == 'aggregation':
            return cls._standard_check(field, value, cls._allow_aggregation)

    _allowed_fields = [
        'strong', 'italic', 'strike',
        'underline', 'horizontal_align', 'vertical_align',
        'editable', 'size', 'kind',
        'number_format',
        'aggregation'
    ]
    _allowed_horizontal_align = [None, 'left', 'center', 'right']
    _allowed_vertical_align = [None, 'top', 'middle', 'bottom']
    _allowed_underline = [None, 'single', 'double', 'single_accounting', 'double_accounting']
    _allowed_kinds = [kind[0] for kind in Cell.KIND_VALUE]
    _allow_aggregation = [None, *[kind[0] for kind in Cell.KIND_AGGREGATION]]

    @staticmethod
    def _get_value_error_message(field: str, value: str, allowed_values: list[str | None]) -> str:
        """Получение сообщения ошибки для значения."""
        str_allowed_values = ', '.join(['null' if v is None else v for v in allowed_values])
        return f'Значение свойства {field} не в списке разрешенных: {value} -> {str_allowed_values}.'

    @classmethod
    def _standard_check(cls, field: str, value: str, allowed_values: list[str | None]) -> Success | Error:
        """Проверка для большинства случаев."""
        if value in allowed_values:
            return cls.Success(value)
        return cls.Error('value', cls._get_value_error_message(field, value, allowed_values))


def get_aggregation_cells(user: User, cell: Cell) -> list[Cell]:
    """Возвращаем ячейки, от которых зависит cell."""
    can_change_period_sheet(user, cell.row.sheet.period)
    to_cells = cell.to_cells.select_related('from_cell').all()
    return [to_cell.from_cell for to_cell in to_cells]


def change_cell_default(user: User, cell: Cell, default: str) -> Cell:
    """Изменение значения ячейки по умолчанию."""
    can_change_period_sheet(user, cell.row.sheet.period)
    cell.default = default
    cell.save(update_fields=('default', 'is_template',))
    return cell


def success_check_cell_options(user: User, cells: QuerySet[Cell]) -> QuerySet[Cell]:
    if len(set(cells.values_list('row__sheet__period', flat=True))) != 1:
        raise PermissionDenied('Ошибка доступа')
    can_change_period_sheet(user, cells.first().row.sheet.period)
    return cells


@transaction.atomic
def change_cells_option(cells: Sequence[Cell], field: str, value:  str | int | bool | None) -> list[dict]:
    """Изменение свойств ячеек."""
    result: list[dict] = []
    for cell in cells:
        update_fields = [field]
        if field == 'kind' and value == 'fl':
            cell.default = 'Нет'
            update_fields.append('default')
            values = list(Value.objects.filter(column__id=cell.column_id, row__id=cell.row_id).all())
            for val in values:
                val.payload = None
                val.value = 'Нет'
            Value.objects.bulk_update(values, ('payload', 'value',))
            result.append({'cell_id': cell.id, 'field': 'value', 'value': cell.default})
        setattr(cell, field, value)
        cell.save(update_fields=update_fields)
        result.append({'cell_id': cell.id, 'field': camelcase(field), 'value': value})
    return result


def add_budget_classification(user: User, code: str, name: str) -> BudgetClassification:
    """Добавления КБК в словарь."""
    can_add_budget_classification(user)
    return BudgetClassification.objects.create(code=code, name=name)
