from datetime import datetime
from os import path
from pathlib import Path
from typing import Any, cast
from zipfile import ZipFile

from devind_core.models import File
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.timezone import make_aware
from openpyxl.utils import get_column_letter

from apps.core.models import User
from apps.dcis.models import Cell, Document, RowDimension, Sheet, Value


def update_or_create_value(
    document: Document,
    sheet: Sheet,
    column_id: int,
    row_id: int,
    value: str,
    payload: Any = None
) -> tuple[Value, bool]:
    """Создание или обновление значения."""
    val, created = Value.objects.update_or_create(
        column_id=column_id,
        row_id=row_id,
        document=document,
        sheet=sheet,
        defaults={
            'value': value,
            'payload': payload
        }
    )
    RowDimension.objects.filter(pk=row_id).update(updated_at=make_aware(datetime.now()))
    return val, created


def update_or_create_file_value(
    user: User,
    document: Document,
    sheet: Sheet,
    column_id: int,
    row_id: int,
    value: str,
    remaining_files: list[int],
    new_files: list[InMemoryUploadedFile],
) -> tuple[Value, bool]:
    """Изменение файлов значения ячейки типа `Файл`."""
    payload = [*remaining_files]
    for new_file in new_files:
        payload.append(File.objects.create(
            name=new_file.name,
            src=new_file,
            deleted=True,
            user=user
        ).pk)
    return update_or_create_value(document, sheet, column_id, row_id, value, payload)


def updates_values_by_cell_kind_change(cell: Cell) -> list[Value]:
    """Изменение значений из-за изменения типа ячейки."""
    values = []
    if cell.kind == Cell.FILES:
        values = list(Value.objects.filter(column__id=cell.column_id, row__id=cell.row_id).all())
        for value in values:
            value.payload = None
            value.value = 'Нет'
        Value.objects.bulk_update(values, ('payload', 'value',))
    return values


def get_file_value_payload(value: Value) -> list[int]:
    """Получение дополнительных данных значения ячейки типа `Файл`."""
    if value.payload is None:
        return []
    return cast(list[int], value.payload)


def get_file_value_files(value: Value) -> list[File]:
    """Получение файлов значения ячейки типа `Файл`."""
    payload = get_file_value_payload(value)
    files = File.objects.filter(pk__in=payload)
    return sorted(files, key=lambda file: payload.index(file.pk))


def create_file_value_archive(value: Value) -> str:
    """Создание архива значения ячейки типа `Файл`."""
    cell = f'{get_column_letter(value.column.index)}{value.row.index}'
    archive_path = f'{path.join(settings.TEMP_FILES_DIR, cell)}.zip'
    with ZipFile(archive_path, 'w') as zip_file:
        for file in get_file_value_files(value):
            zip_file.write(file.src.path, path.basename(file.src.path))
    return f'/{Path(path.relpath(archive_path, settings.BASE_DIR)).as_posix()}'