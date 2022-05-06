from typing import Optional

from django.db.models import F, Q

from apps.core.models import User
from apps.dcis.models.sheet import Cell, Document, MergedCell, RowDimension, Sheet, Value


class RowsUploader:
    """Выгрузчик строк листа."""

    def __init__(self, sheet: Sheet, document_id: Optional[str] = None) -> None:
        self.sheet = sheet
        self.document_id = document_id

    def upload(self) -> list[dict]:
        """Выгрузка строк листа."""
        raw_rows = self._upload_rows()
        row_trees = self._add_row_names(self._connect_rows(raw_rows))
        rows = self._sort_rows(row_trees)
        raw_cells = self._upload_cells(rows)
        raw_values = self._upload_values()
        cells = self._add_cell_values(raw_cells, raw_values)
        return self._add_cells(rows, cells)

    def _upload_rows(self) -> list[dict]:
        """Выгрузка необработанных строк листа."""
        if self.document_id is None:
            rows = self.sheet.rowdimension_set.filter(parent__isnull=True)
        else:
            rows = self.sheet.rowdimension_set.filter(
                Q(parent__isnull=True) | Q(parent__isnull=False, document_id=self.document_id)
            )
        return list(
            rows.values(
                'id', 'index', 'height',
                'fixed', 'hidden', 'dynamic',
                'aggregation', 'created_at', 'updated_at',
                'parent_id', 'document_id', 'user',
            )
        )

    @staticmethod
    def _upload_cells(rows: list[dict]) -> list[dict]:
        """Выгрузка ячеек листа."""
        return list(
            Cell.objects.filter(row__in=[row['id'] for row in rows]).values(
                'id', 'kind', 'editable',
                'formula', 'comment', 'default',
                'mask', 'tooltip', 'column_id',
                'row_id', 'horizontal_align', 'vertical_align',
                'size', 'strong', 'italic',
                'strike', 'underline', 'color',
                'background', 'border_style', 'border_color'
            )
        )

    def _upload_values(self) -> list[dict]:
        """Получение значений листа."""
        if self.document_id is None:
            values = Value.objects.none()
        else:
            values = self.sheet.value_set.filter(document_id=self.document_id)
        return list(values.values('column_id', 'row_id', 'value', 'verified', 'error'))

    @staticmethod
    def _connect_rows(rows: list[dict]) -> list[dict]:
        """Создание деревьев строк."""
        for row in rows:
            row['parent'] = None
            row['children'] = []
        trees = [row for row in rows if row['parent_id'] is None]
        for root in trees:
            root['children'] = [row for row in rows if row['parent_id'] == root['id']]
            for child in root['children']:
                child['parent'] = root
        return trees

    @classmethod
    def _get_row_name(cls, row: dict, indices: Optional[list[int]] = None) -> str:
        """Получение имени строки."""
        indices = indices or []
        if row['parent'] is not None:
            return cls._get_row_name(row['parent'], [str(row['index']), *indices])
        return '.'.join([str(row['index']), *indices])

    @classmethod
    def _add_row_names(cls, rows_tree: list[dict]) -> list[dict]:
        """Добавление имен к строкам."""
        for row in rows_tree:
            row['name'] = cls._get_row_name(row)
            if len(row['children']):
                cls._add_row_names(row['children'])
        return rows_tree

    @classmethod
    def _sort_rows(cls, rows_tree: list[dict]) -> list[dict]:
        """Сортировка строк и добавление глобальных индексов."""
        result: list[dict] = []
        for row in sorted(rows_tree, key=lambda r: r['index']):
            result.append(row)
            result.extend(cls._sort_rows(row['children']))
        for i, row in enumerate(result, 1):
            row['global_index'] = i
        return result

    @staticmethod
    def _add_cell_values(cells: list[dict], values: list[dict]) -> list[dict]:
        """Добавление значений к ячейкам."""
        for raw_cell in cells:
            default = raw_cell['default']
            del raw_cell['default']
            value = next(
                (value for value in values
                 if value['row_id'] == raw_cell['row_id'] and value['column_id'] == raw_cell['column_id']),
                None
            )
            if value is not None:
                raw_cell.update(value)
            else:
                raw_cell.update({'value': default, 'verified': True, 'error': None})
        return cells

    @staticmethod
    def _add_cells(rows: list[dict], cells: list[dict]) -> list[dict]:
        """Добавление ячеек к строкам."""
        for row in rows:
            row['cells'] = [cell for cell in cells if cell['row_id'] == row['id']]
        return rows


def add_row(
    user: User,
    document: Document,
    sheet: Sheet,
    parent_id: Optional[int],
    index: int
) -> tuple[RowDimension, list[Cell], list[MergedCell]]:
    """Добавление строки.

    После добавления строки, строка приобретает новый индекс,
    соответственно, все строки после вставленной строки должны увеличить свой индекс на единицу.
    """
    if parent_id:
        rows = RowDimension.objects.filter(parent_id=parent_id)
    else:
        rows = sheet.rowdimension_set
    rows.filter(index__gte=index).update(index=F('index') + 1)
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
    return row_dimension, cells, sheet.mergedcell_set.all()


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
