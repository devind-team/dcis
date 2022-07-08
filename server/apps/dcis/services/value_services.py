"""Файл, содержащий сервисы для изменения значений ячеек."""
from datetime import datetime
from os import path
from pathlib import Path
from typing import Any, cast, NamedTuple
from zipfile import ZipFile


from django.db.models import QuerySet
from devind_core.models import File
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.timezone import now

from apps.core.models import User
from apps.dcis.models import Value, Sheet, RowDimension, Document, Cell
from apps.dcis.helpers.cell import get_dependency_cells, resolve_cells, resolve_evaluate_state


class UpdateOrCrateValueResult(NamedTuple):
    """Результат создания или обновления значения."""
    value: Value
    updated_at: datetime
    created: bool


class UpdateOrCrateValuesResult(NamedTuple):
    """Результат создания или обновления значения."""
    values: list[Value]
    updated_at: datetime


def update_or_create_value(
    document: Document,
    cell: Cell,
    sheet_id: int | str,
    value: str,
    payload: Any = None
) -> UpdateOrCrateValuesResult:
    """Создание или обновление значения."""
    val, created = Value.objects.update_or_create(
        column_id=cell.column_id,
        row_id=cell.row_id,
        document=document,
        sheet_id=sheet_id,
        defaults={
            'value': value,
            'payload': payload
        }
    )
    values = recalculate_cells(document, val)
    updated_at = now()
    RowDimension.objects.filter(pk=cell.row_id).update(updated_at=updated_at)
    return UpdateOrCrateValuesResult(values=values, updated_at=updated_at)


def recalculate_cells(document: Document, value: Value) -> list[Value]:
    """Пересчитываем значения ячеек в зависимости от новых."""
    from pprint import pprint
    sheets: list[Sheet] = document.sheets.all()
    dependency_cells, inversion_cells = get_dependency_cells(sheets, value)
    cells, values = resolve_cells(sheets, document, {*dependency_cells, *inversion_cells})
    state = resolve_evaluate_state(value.sheet, cells, values, inversion_cells)
    pprint(state)

    # state: dict[str, str | int | float] = resolve_cells_state()
    # evaluate_values: dict[str, str | int | float] = evaluate_sheet(state)
    # values = update_values(sheets, evaluate_values)
    # return values
    return []


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
