import re
from argparse import ArgumentTypeError
from datetime import datetime
from os import path
from pathlib import Path
from typing import Any, NamedTuple, Sequence, cast
from zipfile import ZipFile

from devind_core.models import File
from devind_helpers.utils import convert_str_to_bool, convert_str_to_int
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.db.models import F
from django.utils.timezone import now
from stringcase import camelcase
from xlsx_evaluate.tokenizer import ExcelParser, f_token

from apps.core.models import User
from apps.dcis.models import Period, RowDimension, Sheet, Value
from apps.dcis.models.sheet import Cell, ColumnDimension
from apps.dcis.services.sheet_unload_services import SheetColumnsUnloader, SheetPartialRowsUploader


@transaction.atomic
def rename_sheet(sheet: Sheet, name: str) -> tuple[Sheet, list[Cell]]:
    """Переименование листа с учетом формул.

    sheet.name -> name

    :param sheet - лист
    :param name - новое имя листа
    """
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
    column_dimension: ColumnDimension,
    width: int | None,
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
    document_id: str | int,
    parent_id: int | None,
    index: int,
    global_index: int,
    global_indices_map: dict[int, int]
) -> dict:
    """Добавление строки.

    После добавления строки, строка приобретает новый индекс,
    соответственно, все строки после вставленной строки должны увеличить свой индекс на единицу.
    """
    sheet.rowdimension_set.filter(parent_id=parent_id, index__gte=index).update(index=F('index') + 1)
    row_dimension = RowDimension.objects.create(
        sheet=sheet,
        index=index,
        document_id=document_id,
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
    height: int,
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


@transaction.atomic
def delete_row_dimension(row_dimension: RowDimension) -> int:
    """Удаление строки.

    После удаления строки, все строки после удаленной строки должны уменьшить свой индекс на единицу.
    """
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


class UpdateOrCrateValueResult(NamedTuple):
    """Результат создания или обновления значения."""
    value: Value
    updated_at: datetime
    created: bool


def update_or_create_value(
    document_id: int | str,
    sheet_id: int | str,
    column_id: int | str,
    row_id: int | str,
    value: str,
    payload: Any = None
) -> UpdateOrCrateValueResult:
    """Создание или обновление значения."""
    val, created = Value.objects.update_or_create(
        column_id=column_id,
        row_id=row_id,
        document_id=document_id,
        sheet_id=sheet_id,
        defaults={
            'value': value,
            'payload': payload
        }
    )
    updated_at = now()
    RowDimension.objects.filter(pk=row_id).update(updated_at=updated_at)
    return UpdateOrCrateValueResult(value=val, updated_at=updated_at, created=created)


def update_or_create_file_value(
    user: User,
    document_id: int | str,
    sheet_id: int | str,
    column_id: int | str,
    row_id: int | str,
    value: str,
    remaining_files: list[int],
    new_files: list[InMemoryUploadedFile],
) -> UpdateOrCrateValueResult:
    """Изменение файлов значения ячейки типа `Файл`."""
    payload = [*remaining_files]
    for new_file in new_files:
        payload.append(File.objects.create(
            name=new_file.name,
            src=new_file,
            deleted=True,
            user=user
        ).pk)
    return update_or_create_value(document_id, sheet_id, column_id, row_id, value, payload)


def create_file_value_archive(value: Value, name: str) -> str:
    """Создание архива значения ячейки типа `Файл`."""
    archive_path = f'{path.join(settings.TEMP_FILES_DIR, name)}.zip'
    with ZipFile(archive_path, 'w') as zip_file:
        for file in get_file_value_files(value):
            zip_file.write(file.src.path, path.basename(file.src.path))
    return f'/{Path(path.relpath(archive_path, settings.BASE_DIR)).as_posix()}'


def get_file_value_files(value: Value) -> list[File]:
    """Получение файлов значения ячейки типа `Файл`."""
    payload = get_file_value_payload(value)
    files = File.objects.filter(pk__in=payload)
    return sorted(files, key=lambda file: payload.index(file.pk))


def get_file_value_payload(value: Value) -> list[int]:
    """Получение дополнительных данных значения ячейки типа `Файл`."""
    if value.payload is None:
        return []
    return cast(list[int], value.payload)


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
