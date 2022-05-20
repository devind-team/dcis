from typing import Optional

from django.db.models import F

from apps.core.models import User
from apps.dcis.models.sheet import Cell, Document, RowDimension, Sheet
from apps.dcis.services.sheet_unload_services import SheetColumnsUnloader, SheetPartialRowsUploader


def add_row(
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
