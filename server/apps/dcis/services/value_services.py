"""Файл, содержащий сервисы для изменения значений ячеек."""

from datetime import datetime
from os import path
from pathlib import Path
from typing import Any, NamedTuple, cast
from zipfile import ZipFile

from devind_core.models import File
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.timezone import now

from apps.core.models import User
from apps.dcis.helpers.cell import (
    ValueState, evaluate_state, get_dependency_cells, resolve_cells,
    resolve_evaluate_state,
)
from apps.dcis.helpers.sheet_formula_cache import SheetFormulaContainerCache
from apps.dcis.models import Cell, Document, RowDimension, Sheet, Value
from apps.dcis.permissions import can_view_document


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
    Document.objects.filter(pk=document.pk).update(updated_at=updated_at)
    return UpdateOrCrateValuesResult(values=values, updated_at=updated_at)


def recalculate_cells(document: Document, value: Value) -> list[Value]:
    """Пересчитываем значения ячеек в зависимости от новых."""
    sheets: list[Sheet] = document.sheets.all()
    sheet_containers: list[SheetFormulaContainerCache] = [SheetFormulaContainerCache.get(sheet) for sheet in sheets]
    # 1. Собираем зависимости и последовательность операций
    dependency_cells, inversion_cells, sequence_evaluate = get_dependency_cells(sheet_containers, value)
    # 1.1 Если у нас нет ячеек необходимых для пересчета, возвращаем только само значение
    if not inversion_cells:
        return [value]
    # 2. Получаем связанные ячейки и значения из базы данных
    cells, values = resolve_cells(sheets, document, {*dependency_cells, *inversion_cells})
    # 3. Строим изначальное состояние всех значений
    state: dict[str, ValueState] = resolve_evaluate_state(cells, values, inversion_cells)
    # 4. Рассчитываем значения
    evaluate_result: dict[str, ValueState] = evaluate_state(state, sequence_evaluate)
    # 5. Сохраняем значения
    result_values: list[Value] = []
    for cell_name, result_value in evaluate_result.items():
        cell: Cell = result_value['cell']
        if (
                result_value['value'] is None or
                cell_name not in inversion_cells or
                cell.column_id == value.column_id and
                cell.row_id == value.row_id and
                cell.column.sheet_id == value.sheet_id
        ):
            continue
        val, created = Value.objects.update_or_create(
            column_id=cell.column_id,
            row_id=cell.row_id,
            sheet_id=cell.column.sheet_id,
            document=document,
            defaults={
                'value': result_value['value'],
                'error': result_value['error'],
            }
        )
        result_values.append(val)
    return [value, *result_values]


def update_or_create_file_value(
    user: User,
    document: Document,
    cell: Cell,
    sheet_id: int | str,
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
        column_id=cell.column_id,
        row_id=cell.row_id,
        sheet_id=sheet_id,
        document=document,
        defaults={
            'value': value,
            'payload': payload
        }
    )
    updated_at = now()
    RowDimension.objects.filter(pk=cell.row_id).update(updated_at=updated_at)
    Document.objects.filter(pk=document.pk).update(updated_at=updated_at)
    return UpdateOrCrateValueResult(value=val, updated_at=updated_at, created=created)


def create_file_value_archive(user: User, document: Document, value: Value, name: str) -> str:
    """Создание архива значения ячейки типа `Файл`."""
    can_view_document(user, document)
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
