"""Модуль, отвечающий за работу со строками."""
from typing import Any

from django.db import transaction
from django.db.models import F, Max, Min

from apps.core.models import User
from apps.dcis.models import Document, RowDimension, Sheet
from apps.dcis.models.sheet import Cell, MergedCell
from apps.dcis.permissions import (
    can_add_child_row_dimension,
    can_change_child_row_dimension_height,
    can_change_period_sheet,
    can_delete_child_row_dimension,
)
from apps.dcis.services.sheet_unload_services import SheetColumnsUnloader, SheetPartialRowsUploader


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


@transaction.atomic
def change_row_dimension(
    user: User,
    row_dimension: RowDimension,
    height: int,
    hidden: bool,
    dynamic: bool,
) -> RowDimension:
    """Изменение строки."""
    can_change_period_sheet(user, row_dimension.sheet.period)
    row_dimension.height = height
    row_dimension.hidden = hidden
    row_dimension.dynamic = dynamic
    row_dimension.save(update_fields=('height', 'hidden', 'dynamic', 'updated_at'))
    return row_dimension


def change_row_dimensions_fixed(row_dimensions: list[RowDimension], fixed: bool) -> list[RowDimension]:
    """Изменение свойства fixed у строк.

    При изменении фиксации, фиксация также меняется у строк, которые делят общую ячейку со строкой.
    """
    change_rows = set()
    for row_dimension in row_dimensions:
        change_rows.update(get_relative_rows(row_dimension))
    for row in change_rows:
        row.fixed = fixed
    RowDimension.objects.bulk_update(change_rows, ('fixed',))
    return list(change_rows)


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


def get_relative_rows(row_dimension: RowDimension) -> list[RowDimension]:
    """Получение строк, которые делят общую ячейку со строкой `row_dimension`."""
    merged_cell = MergedCell.objects.filter(
        sheet=row_dimension.sheet,
        min_row__lte=row_dimension.index,
        max_row__gte=row_dimension.index,
    )
    if merged_cell.count() == 0:
        return [row_dimension]
    min_max = merged_cell.aggregate(min=Min('min_row'), max=Max('max_row'))
    return list(RowDimension.objects.filter(
        sheet=row_dimension.sheet,
        document=row_dimension.document,
        index__in=range(min_max['min'], min_max['max'] + 1)
    ))


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
