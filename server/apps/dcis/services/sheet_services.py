from apps.dcis.models.sheet import Sheet


def move_merged_cells(sheet: Sheet, idx: int, offset: int, delete: bool = False):
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
