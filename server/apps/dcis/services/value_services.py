"""Файл, содержащий сервисы для изменения значений ячеек."""

from dataclasses import dataclass
from datetime import datetime
from os import path
from pathlib import Path
from typing import cast
from zipfile import ZipFile

from devind_core.models import File
from devind_dictionaries.models import Department, Organization
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.utils.timezone import now

from apps.core.models import User
from apps.dcis.helpers.cell import (
    ValueState,
    evaluate_state,
    get_dependency_cells,
    resolve_cells,
    resolve_evaluate_state,
)
from apps.dcis.helpers.sheet_formula_cache import SheetFormulaContainerCache
from apps.dcis.models import Cell, Document, Period, RowDimension, Sheet, Value
from apps.dcis.permissions import can_view_document
from apps.dcis.services.cell_service import calculate_aggregation_cell


@dataclass
class FileValue:
    """Значение ячейки типа `Файл`."""
    remaining_files: list[int]
    new_files: list[InMemoryUploadedFile]


@dataclass
class ValueInput:
    """Значение ячейки для создания или обновления."""
    cell: Cell
    value: str


@dataclass
class UpdateOrCrateValueResult:
    """Результат создания или обновления значения."""
    value: Value
    updated_at: datetime
    created: bool


@dataclass
class UpdateOrCrateValuesResult:
    """Результат создания или обновления значения."""
    values: list[Value]
    updated_at: datetime


def update_or_create_values(
    user: User,
    document: Document,
    sheet_id: int | str,
    values: list[ValueInput]
) -> UpdateOrCrateValuesResult:
    """Создание или обновление значений."""
    vals: list[Value] = []
    for value in values:
        vals.extend(recalculate_aggregations(document, sheet_id, value))
    vals = recalculate_cells(document, vals)
    updated_at = now()
    RowDimension.objects.filter(pk__in=[val.row_id for val in vals]).update(updated_at=updated_at)
    Document.objects.filter(pk=document.pk).update(updated_at=updated_at, updated_by=user)
    return UpdateOrCrateValuesResult(values=vals, updated_at=updated_at)


def update_or_create_value(
    document: Document,
    sheet_id: int | str,
    value: ValueInput,
    extra_value: str | None = None
) -> Value:
    """Создание или обновления значения."""
    extra = {'extra_value': extra_value} if extra_value else {}
    vl, _ = Value.objects.update_or_create(
        column_id=value.cell.column_id,
        row_id=value.cell.row_id,
        document=document,
        sheet_id=sheet_id,
        defaults={
            'value': value.value,
            **extra
        }
    )
    return vl


def recalculate_aggregations(document: Document, sheet_id: int, value: ValueInput) -> list[Value]:
    """Пересчитываем агрегирующие ячейки.

    Ячейка Cell, которая является источником, то есть, нужно выбирать по потоку следования:
        cell выбираем по from_cells - является исходящей для to_cells - целевые
    """
    if not value.cell.is_aggregation:
        # Если ячейка не агрегирующая, просто возвращаем ее обновленное значение
        return [update_or_create_value(document, sheet_id, value)]
    # 1. Так как ячейка аградационная, ее значение попадает в extra_value
    # 2. А вот value мы должны вычислить value = fn(extra_value, *aggregation_cells)
    period = Period.objects.select_related('project').get(pk=document.period_id)
    # 3. Проверяем, могут ли быть ли дочерние элементы, если дивизион не может содержать дочерние, то и агрегации нет
    if not hasattr(period.project.division, 'parent_id'):
        return [update_or_create_value(document, sheet_id, value)]
    divisions_id = period.project.division.objects.filter(parent_id=document.object_id).values_list('pk', flat=True)
    if divisions_id:
        # 1. Дочерние дивизионы найдены, значит мы головная организация
        source_cells = [relation_cell.from_cell for relation_cell in value.cell.to_cells.all()]
        extra_value = value.value
        if source_cells:
            cells_filter = Q()
            # 2. Собираем фильтр для значений
            for source_cell in source_cells:
                cells_filter |= Q(column_id=source_cell.column_id, row_id=source_cell.row_id)
            # 3. Собираем фильтр по дивизионам и версии документа
            children_documents = Document.objects.filter(
                period=period, version=document.version, object_id__in=divisions_id
            ).values_list('pk', flat=True)
            values_filter = Q()
            for child_document in children_documents:
                values_filter |= Q(document=child_document) & cells_filter
            values = Value.objects.filter(values_filter).values_list('value', flat=True)
            value = calculate_aggregation_cell(value.cell, extra_value, *values)
        vals = [update_or_create_value(document, sheet_id, value, extra_value)]
    else:
        # 4. Если у нас не найдены дочерние документы, то пишем в value
        vals = [update_or_create_value(document, sheet_id, value)]

    # 4. Проверяем если ячейки зависят от нас
    division: Organization | Department = period.project.division.objects.get(pk=document.object_id)
    parent_document: Document | None = Document.objects.filter(
        period=document.period,
        version=document.version,
        object_id=division.parent_id
    ).first()
    # 5. Если у дивизиона нет родителя и нет документа
    if division.parent is None or parent_document is None:
        return vals
    target_cells = [relation_cell.to_cell for relation_cell in value.cell.from_cells.all()]
    for target_cell in target_cells:
        target_val: Value | None = Value.objects.filter(
            document=parent_document,
            column_id=target_cell.column_id,
            row_id=target_cell.row_id
        ).first()
        if target_val:
            target_value = target_val.extra_value if target_cell.is_aggregation else target_val.value
        else:
            target_value = '0'
        vals.extend(recalculate_aggregations(
            parent_document,
            target_cell.column.sheet_id,
            ValueInput(cell=target_cell, value=target_value)
        ))
    return vals


def recalculate_cells(document: Document, values: list[Value]) -> list[Value]:
    """Пересчитываем значения ячеек в зависимости от новых."""
    sheets: list[Sheet] = document.sheets.all()
    sheet_containers: list[SheetFormulaContainerCache] = [SheetFormulaContainerCache.get(sheet) for sheet in sheets]
    # 1. Собираем зависимости и последовательность операций
    dependency_cells, inversion_cells, sequence_evaluate = get_dependency_cells(sheet_containers, values)
    # 1.1 Если у нас нет ячеек необходимых для пересчета, возвращаем только само значение
    if not inversion_cells:
        return values
    # 2. Получаем связанные ячейки и значения из базы данных
    cells, values = resolve_cells(sheets, document, {*dependency_cells, *inversion_cells})
    # 3. Строим изначальное состояние всех значений
    state: dict[str, ValueState] = resolve_evaluate_state(cells, values, inversion_cells)
    # 4. Рассчитываем значения
    evaluate_result: dict[str, ValueState] = evaluate_state(state, sequence_evaluate)
    # 5. Сохраняем значения
    result_values: list[Value] = []
    for cell_name, result_value in evaluate_result.items():
        cell = result_value['cell']
        if (
            result_value['value'] is None or
            cell_name not in inversion_cells or
            next((
                value for value in values if
                cell.column_id == value.column_id and
                cell.row_id == value.row_id and
                cell.column.sheet_id == value.sheet_id
            ), None) is None
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
    return [*values, *result_values]


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
    Document.objects.filter(pk=document.pk).update(updated_at=updated_at, updated_by=user)
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
