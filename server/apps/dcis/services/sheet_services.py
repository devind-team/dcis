import re
from argparse import ArgumentTypeError
from typing import Any, NamedTuple, Sequence

from devind_dictionaries.models import BudgetClassification
from devind_helpers.exceptions import PermissionDenied
from devind_helpers.utils import convert_str_to_bool, convert_str_to_int
from django.db import transaction
from django.db.models import F, QuerySet
from stringcase import camelcase
from xlsx_evaluate.tokenizer import ExcelParser, f_token

from apps.core.models import User
from apps.dcis.models import Document, Period, RowDimension, Sheet, Value
from apps.dcis.models.sheet import Cell, ColumnDimension
from apps.dcis.permissions import (
    can_add_budget_classification,
    can_add_child_row_dimension,
    can_change_child_row_dimension_height,
    can_change_period_sheet,
    can_delete_child_row_dimension
)
from apps.dcis.services.sheet_unload_services import SheetColumnsUnloader, SheetPartialRowsUploader


@transaction.atomic
def rename_sheet(user: User, sheet: Sheet, name: str) -> tuple[Sheet, list[Cell]]:
    """Переименование листа с учетом формул.

    sheet.name -> name

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


def change_column_dimension(
    user: User,
    column_dimension: ColumnDimension,
    width: int | None,
    fixed: bool,
    hidden: bool,
    kind: str
) -> ColumnDimension:
    """Изменение колонки."""
    can_change_period_sheet(user, column_dimension.sheet.period)
    column_dimension.width = width
    column_dimension.fixed = fixed
    column_dimension.hidden = hidden
    column_dimension.kind = kind
    column_dimension.save(update_fields=('width', 'fixed', 'hidden', 'kind', 'updated_at'))
    return column_dimension


@transaction.atomic
def add_row_dimension(
    user: User,
    sheet: Sheet,
    index: int,
    global_index: int,
    global_indices_map: dict[int, int]
) -> dict:
    """Добавление строки.

    После добавления строки, строка приобретает новый индекс,
    соответственно, все строки после вставленной строки должны увеличить свой индекс на единицу.
    """
    can_change_period_sheet(user, sheet.period)
    sheet.rowdimension_set.filter(parent_id=None, index__gte=index).update(index=F('index') + 1)
    row_dimension = RowDimension.objects.create(
        sheet=sheet,
        index=index,
        user=user
    )
    cells = [
        Cell.objects.create(row=row_dimension, column=column, kind=column.kind)
        for column in sheet.columndimension_set.all()
    ]
    move_merged_cells(sheet, index, 1)
    return SheetPartialRowsUploader(
        columns_unloader=SheetColumnsUnloader(sheet.columndimension_set.all()),
        rows=[row_dimension],
        cells=cells,
        merged_cells=sheet.mergedcell_set.all(),
        values=[],
        rows_global_indices_map={**global_indices_map, row_dimension.id: global_index},
    ).unload()[0]


@transaction.atomic
def add_child_row_dimension(
        user: User,
        context: Any,
        sheet: Sheet,
        document: Document,
        parent: RowDimension,
        index: int,
        global_index: int,
        global_indices_map: dict[int, int]
) -> dict:
    """Добавление дочерней строки.

    После добавления строки, строка приобретает новый индекс,
    соответственно, все строки после вставленной строки должны увеличить свой индекс на единицу.
    """
    can_add_child_row_dimension(
        user,
        document=document,
        row_dimension=parent
    )
    sheet.rowdimension_set.filter(parent=parent, document=document, index__gte=index).update(index=F('index') + 1)
    row_dimension = RowDimension.objects.create(
        sheet=sheet,
        index=index,
        document=document,
        parent=parent,
        dynamic=True,
        user=context.user
    )
    cells = [
        Cell.objects.create(row=row_dimension, column=column, kind=column.kind)
        for column in sheet.columndimension_set.all()
    ]
    return SheetPartialRowsUploader(
        columns_unloader=SheetColumnsUnloader(sheet.columndimension_set.all()),
        rows=[row_dimension],
        cells=cells,
        merged_cells=sheet.mergedcell_set.all(),
        values=[],
        rows_global_indices_map={**global_indices_map, row_dimension.id: global_index},
    ).unload()[0]


def change_row_dimension(
        user: User,
        row_dimension: RowDimension,
        height: int,
        fixed: bool,
        hidden: bool,
        dynamic: bool
) -> RowDimension:
    """Изменение строки."""
    can_change_period_sheet(user, row_dimension.sheet.period)
    row_dimension.height = height
    row_dimension.fixed = fixed
    row_dimension.hidden = hidden
    row_dimension.dynamic = dynamic
    row_dimension.save(update_fields=('height', 'fixed', 'hidden', 'dynamic', 'updated_at'))
    return row_dimension


def change_row_dimension_height(user: User, row_dimension: RowDimension, height: int) -> RowDimension:
    """Изменение высоты строки."""
    can_change_child_row_dimension_height(user, row_dimension)
    row_dimension.height = height
    row_dimension.save(update_fields=('height', 'updated_at'))
    return row_dimension


@transaction.atomic
def delete_row_dimension(user: User, row_dimension: RowDimension) -> int:
    """Удаление строки.

    После удаления строки, все строки после удаленной строки должны уменьшить свой индекс на единицу.
    """
    can_change_period_sheet(user, row_dimension.sheet.period)
    can_delete_child_row_dimension(user, row_dimension)
    row_dimension_id = row_dimension.id
    row_dimension.delete()
    row_dimension.sheet.rowdimension_set.filter(
        parent_id=row_dimension.parent_id,
        index__gt=row_dimension.index,
    ).update(index=F('index') - 1)
    if not row_dimension.parent_id:
        move_merged_cells(row_dimension.sheet, row_dimension.index, -1, True)
    return row_dimension_id


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
        if field in ['strong', 'italic', 'strike']:
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

    _allowed_fields = ['strong', 'italic', 'strike', 'underline', 'horizontal_align', 'vertical_align', 'size', 'kind']
    _allowed_horizontal_align = [None, 'left', 'center', 'right']
    _allowed_vertical_align = [None, 'top', 'middle', 'bottom']
    _allowed_underline = [None, 'single', 'double', 'single_accounting', 'double_accounting']
    _allowed_kinds = [kind[0] for kind in Cell.KIND_VALUE]

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


def change_cell_default(user: User, cell: Cell, default: str) -> Cell:
    """Изменение значения ячейки по умолчанию."""
    can_change_period_sheet(user, cell.row.sheet.period)
    cell.default = default
    cell.save(update_fields=('default',))
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


def move_merged_cells(sheet: Sheet, idx: int, offset: int, delete: bool = False) -> None:
    """Двигаем объединенные строки в зависимости от добавления или удаления.

    В будущем метод нужно сделать универсальным (и для колонок).
    """
    for merge_cells in sheet.mergedcell_set.all():
        if merge_cells.min_row <= idx <= merge_cells.max_row:
            merge_cells.max_row += offset
            if not delete and merge_cells.min_row == idx:
                merge_cells.min_row += offset
        elif merge_cells.min_row > idx:
            merge_cells.min_row += offset
            merge_cells.max_row += offset
        if merge_cells.min_row > merge_cells.max_row or len(merge_cells.cells) == 1:
            merge_cells.delete()
        else:
            merge_cells.save(update_fields=('min_row', 'max_row',))


def add_budget_classification(user: User, code: str, name: str) -> BudgetClassification:
    """Добавления КБК в словарь."""
    can_add_budget_classification(user)
    return BudgetClassification.objects.create(code=code, name=name)
