from argparse import ArgumentTypeError
from typing import NamedTuple, Optional, Sequence, Union

from devind_helpers.utils import convert_str_to_bool, convert_str_to_int
from django.db import transaction
from django.db.models import F
from stringcase import camelcase

from apps.core.models import User
from apps.dcis.models.sheet import Cell, ColumnDimension, Document, RowDimension, Sheet, Value
from apps.dcis.services.sheet_unload_services import SheetColumnsUnloader, SheetPartialRowsUploader


def change_column_dimension(
    column_dimension: ColumnDimension,
    width: Optional[int],
    fixed: bool,
    hidden: bool,
    kind: str
) -> ColumnDimension:
    """Изменение колонки."""
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
    document: Optional[Document],
    parent_id: Optional[int],
    index: int,
    global_index: int,
    global_indices_map: dict[int, int]
) -> dict:
    """Добавление строки.

    После добавления строки, строка приобретает новый индекс,
    соответственно, все строки после вставленной строки должны увеличить свой индекс на единицу.
    """
    if parent_id:
        rows = RowDimension.objects.filter(parent_id=parent_id)
    else:
        rows = sheet.rowdimension_set
    rows.filter(parent_id=parent_id, index__gte=index).update(index=F('index') + 1)
    row_dimension = RowDimension.objects.create(
        sheet=sheet,
        index=index,
        document=document,
        parent_id=parent_id,
        dynamic=bool(parent_id),
        user=user
    )
    cells = [
        Cell.objects.create(row=row_dimension, column=column, kind=column.kind)
        for column in sheet.columndimension_set.all()
    ]
    if not parent_id:
        move_merged_cells(sheet, index, 1)
    return SheetPartialRowsUploader(
        columns_unloader=SheetColumnsUnloader(sheet.columndimension_set.all()),
        rows=[row_dimension],
        cells=cells,
        merged_cells=sheet.mergedcell_set.all(),
        values=[],
        rows_global_indices_map={**global_indices_map, row_dimension.id: global_index}
    ).unload()[0]


def change_row_dimension(
    row_dimension: RowDimension,
    height: Optional[int],
    fixed: bool,
    hidden: bool,
    dynamic: bool
) -> RowDimension:
    """Изменение строки."""
    row_dimension.height = height
    row_dimension.fixed = fixed
    row_dimension.hidden = hidden
    row_dimension.dynamic = dynamic
    row_dimension.save(update_fields=('height', 'fixed', 'hidden', 'dynamic', 'updated_at'))
    return row_dimension


class CheckCellOptions:
    """Проверка возможности изменения свойств ячеек."""

    class Success(NamedTuple):
        value: Union[str, int, bool]

    class Error(NamedTuple):
        field: str
        error: str

    def __new__(cls, field: str, value: str) -> Union[Success, Error]:
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
    def _get_value_error_message(field: str, value: str, allowed_values: list[Union[str, None]]) -> str:
        """Получение сообщения ошибки для значения."""
        str_allowed_values = ', '.join(['null' if v is None else v for v in allowed_values])
        return f'Значение свойства {field} не в списке разрешенных: {value} -> {str_allowed_values}.'

    @classmethod
    def _standard_check(cls, field: str, value: str, allowed_values: list[Union[str, None]]) -> Union[Success, Error]:
        """Проверка для большинства случаев."""
        if value in allowed_values:
            return cls.Success(value)
        return cls.Error('value', cls._get_value_error_message(field, value, allowed_values))


@transaction.atomic
def change_cells_option(cells: Sequence[Cell], field: str, value: Optional[Union[str, int, bool]]) -> list[dict]:
    """Изменение свойств ячеек."""
    result: list[dict] = []
    for cell in cells:
        update_fields = [field]
        if field == 'kind' and value == 'fl':
            cell.default = 'Нет'
            update_fields.append('default')
            values = list(Value.objects.filter(column__id=cell.column_id, row__id=cell.row_id).all())
            for value in values:
                value.payload = None
                value.value = 'Нет'
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
