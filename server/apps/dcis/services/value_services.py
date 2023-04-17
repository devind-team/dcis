"""Файл, содержащий сервисы для изменения значений ячеек."""

from dataclasses import dataclass
from datetime import datetime
from itertools import groupby, product
from os import path
from pathlib import Path
from typing import Any, Generator, cast
from zipfile import ZipFile

from devind_core.models import File
from devind_dictionaries.models import Organization
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
from apps.dcis.models.sheet import KindCell
from apps.dcis.permissions import can_view_document
from apps.dcis.services.aggregation_services import calculate_aggregation_cell


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
class RecalculationData:
    """Данные для пересчета."""
    cell: Cell
    value: Value
    is_aggregation_recalculated: bool = False


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
    value_inputs: list[ValueInput],
) -> UpdateOrCrateValuesResult:
    """Создание или обновление значений."""
    recalculations: list[RecalculationData] = []
    for value_input in value_inputs:
        value = update_or_create_value(
            document=document,
            sheet_id=sheet_id,
            cell=value_input.cell,
            value=value_input.value
        )
        recalculations.append(RecalculationData(cell=value_input.cell, value=value))
    old_recalculations: list[RecalculationData] = []
    while len(recalculations) != len(old_recalculations):
        old_recalculations = recalculations
        recalculations_copy = recalculations
        recalculations = []
        for doc, recs in group_by_documents(recalculations_copy):
            recalculations.extend(recalculate_aggregations(doc, recs))
        recalculations_copy = recalculations
        recalculations = []
        for doc, recs in group_by_documents(recalculations_copy):
            recalculations.extend(recalculate_values(doc, recs))
    values = [recalculation.value for recalculation in recalculations]
    updated_at = now()
    RowDimension.objects.filter(pk__in=[val.row_id for val in values]).update(updated_at=updated_at)
    Document.objects.filter(pk=document.pk).update(updated_at=updated_at, updated_by=user)
    return UpdateOrCrateValuesResult(values=values, updated_at=updated_at)


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
    archive_path = f'{settings.TEMP_FILES_DIR / name}.zip'
    with ZipFile(archive_path, 'w') as zip_file:
        for file in get_file_value_files(value):
            zip_file.write(file.src.path, path.basename(file.src.path))
    return f'/{Path(path.relpath(archive_path, settings.BASE_DIR)).as_posix()}'


def get_file_value_files(value: Value) -> list[File]:
    """Получение файлов значения ячейки типа `Файл`."""
    payload = get_file_value_payload(value)
    files = File.objects.filter(pk__in=payload)
    return sorted(files, key=lambda file: payload.index(file.pk))


def update_or_create_value(
    document: Document,
    sheet_id: int | str,
    cell: Cell,
    value: str,
    error: str | None = None,
) -> Value:
    """Создание или обновления значения."""
    value, _ = Value.objects.update_or_create(
        column_id=cell.column_id,
        row_id=cell.row_id,
        document=document,
        sheet_id=sheet_id,
        defaults={
            'value': value,
            'error': error
        }
    )
    return value


def recalculate_aggregations(document: Document, recalculations: list[RecalculationData]) -> list[RecalculationData]:
    """Перерасчет агрегации для ячеек."""
    period = Period.objects.select_related('project').get(pk=document.period_id)
    # Проверяем, могут ли быть ли дочерние дивизионы, если дивизион не может содержать дочерние, то и агрегации нет
    if not hasattr(period.project.division, 'parent_id'):
        return recalculations
    recalculated = [r for r in recalculations if r.is_aggregation_recalculated]
    to_recalculate = [r for r in recalculations if not r.is_aggregation_recalculated]
    for recalculation in to_recalculate:
        recalculated.append(recalculate_aggregation(document, recalculation))
    recalculated.extend(recalculate_dependency_aggregation(document, to_recalculate))
    return recalculated


def recalculate_aggregation(document: Document, recalculation: RecalculationData) -> RecalculationData:
    """Расчет агрегации для текущей ячейки."""
    recalculation.is_aggregation_recalculated = True
    # Если ячейка не агрегирующая, оставляем `recalculation` как есть.
    if not recalculation.cell.is_aggregation:
        return recalculation
    division_ids = document.period.project.division.objects.filter(
        parent_id=document.object_id
    ).values_list('pk', flat=True)
    if division_ids:
        # 1. Дочерние дивизионы найдены, значит мы головная организация и необходимо пересчитать агрегацию
        source_cells = [relation_cell.from_cell for relation_cell in recalculation.cell.to_cells.all()]
        if source_cells:
            cells_filter = Q()
            # 2. Собираем фильтр для значений
            for source_cell in source_cells:
                cells_filter |= Q(column_id=source_cell.column_id, row_id=source_cell.row_id)
            # 3. Собираем фильтр по дивизионам и версии документа
            children_documents = Document.objects.filter(
                period=document.period, version=document.version, object_id__in=division_ids
            ).values_list('pk', flat=True)
            values_filter = Q()
            for child_document in children_documents:
                values_filter |= Q(document=child_document) & cells_filter
            vals = Value.objects.filter(values_filter)
            # 4. Добавляем отсутствующие значения
            values: list[str] = []
            for child_document, cell in product(children_documents, source_cells):
                val = next(
                    (v for v in vals if
                     v.column_id == cell.column_id and v.row_id == cell.row_id and v.document_id == child_document),
                    None
                )
                if val is not None:
                    values.append(val.value)
                else:
                    values.append(cell.default or '0.0')
            value = str(calculate_aggregation_cell(recalculation.cell, *values))
            recalculation.value = update_or_create_value(
                document=document,
                sheet_id=cast(int, recalculation.cell.column.sheet_id),
                cell=recalculation.cell,
                value=value,
            )
    return recalculation


def recalculate_dependency_aggregation(
    document: Document,
    recalculations: list[RecalculationData],
) -> list[RecalculationData]:
    """Расчет агрегации для ячеек, которые зависят от текущих."""
    division: Organization = document.period.project.division.objects.get(pk=document.object_id)
    parent_document: Document | None = Document.objects.filter(
        period=document.period,
        version=document.version,
        object_id=division.parent_id
    ).first()
    if parent_document is None:
        return []
    target_cells = set()
    for recalculation in recalculations:
        target_cells.update(relation_cell.to_cell for relation_cell in recalculation.cell.from_cells.all())
    to_recalculate_data: list[RecalculationData] = []
    for target_cell in target_cells:
        target_value: Value | None = Value.objects.filter(
            document=parent_document,
            column_id=target_cell.column_id,
            row_id=target_cell.row_id
        ).first()
        if target_value is None:
            target_value = update_or_create_value(
                document=parent_document,
                sheet_id=target_cell.column.sheet_id,
                cell=target_cell,
                value='0.0',
            )
        to_recalculate_data.append(RecalculationData(cell=target_cell, value=target_value))
    return recalculate_aggregations(parent_document, to_recalculate_data)


def recalculate_values(document: Document, recalculations: list[RecalculationData]) -> list[RecalculationData]:
    """Пересчитываем значения ячеек в зависимости от новых."""
    sheets: list[Sheet] = document.sheets.all()
    sheet_containers: list[SheetFormulaContainerCache] = [SheetFormulaContainerCache.get(sheet) for sheet in sheets]
    # 1. Собираем зависимости и последовательность операций
    dependency_cells, inversion_cells, sequence_evaluate = get_dependency_cells(
        sheet_containers,
        [recalculation.value for recalculation in recalculations if recalculation.cell.kind != KindCell.FORMULA]
    )
    # 1.1 Если у нас нет ячеек необходимых для пересчета, возвращаем изначальные значения
    if not inversion_cells:
        return recalculations
    # 2. Получаем связанные ячейки и значения из базы данных
    cells, resolve_values = resolve_cells(sheets, document, {*dependency_cells, *inversion_cells})
    # 3. Строим изначальное состояние всех значений
    state: dict[str, ValueState] = resolve_evaluate_state(cells, resolve_values, inversion_cells)
    # 4. Рассчитываем значения
    evaluate_result: dict[str, ValueState] = evaluate_state(state, sequence_evaluate)
    # 5. Сохраняем значения
    result_recalculations: list[RecalculationData] = []
    for cell_name, result_value in evaluate_result.items():
        cell = result_value['cell']
        exist_cell = next((
            recalculation for recalculation in recalculations if
            cell.column_id == recalculation.value.column_id and
            cell.row_id == recalculation.value.row_id and
            cell.column.sheet_id == recalculation.value.sheet_id
        ), None)
        if result_value['value'] is None or cell_name not in inversion_cells or exist_cell is not None:
            continue
        value = update_or_create_value(
            document=document,
            sheet_id=cast(int, cell.column.sheet_id),
            cell=cell,
            value=result_value['value'],
            error=result_value['error'],
        )
        result_recalculations.append(RecalculationData(cell=cell, value=value))
    return [*recalculations, *result_recalculations]


def group_by_documents(recalculations: list[RecalculationData]) -> Generator[tuple[Document, list], Any, None]:
    """Группировка данных для пересчета по документам."""
    for _, recs in groupby(sorted(recalculations, key=lambda r: r.value.document.id), lambda r: r.value.document.id):
        recs = list(recs)
        yield recs[0].value.document, recs


def get_file_value_payload(value: Value) -> list[int]:
    """Получение дополнительных данных значения ячейки типа `Файл`."""
    if value.payload is None:
        return []
    return cast(list[int], value.payload)
