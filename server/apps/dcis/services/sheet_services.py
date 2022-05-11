from typing import Optional, Union, Sequence

from django.db.models import F, Q, QuerySet, Model
from django.forms.models import model_to_dict

from apps.core.models import User
from apps.dcis.models.sheet import Cell, Document, MergedCell, RowDimension, Sheet, Value


class RowsUploader:
    """Выгрузчик строк листа."""

    def __init__(
        self,
        rows: Union[QuerySet[RowDimension], Sequence[RowDimension]],
        cells: Union[QuerySet[Cell], Sequence[Cell]],
        values: Union[QuerySet[Value], Sequence[Value]]
    ) -> None:
        self.rows = rows
        self.cells = cells
        self.values = values

    def upload(self) -> list[dict]:
        """Выгрузка строк листа."""
        raw_rows = self._upload_raw_rows()
        raw_cells = self._upload_raw_cells()
        raw_values = self._upload_raw_values()
        row_trees = self._add_row_names(self._connect_rows(raw_rows))
        sorted_rows = self._sort_rows(row_trees)
        cells = self._add_cell_values(raw_cells, raw_values)
        rows = self._add_cells(sorted_rows, cells)
        return rows

    @staticmethod
    def create_sheet_uploader(sheet: Sheet) -> 'RowsUploader':
        """Создание выгрузчика строк листа.

        Выгружает структуру листа без подстрок и значений.
        """
        rows = list(sheet.rowdimension_set.filter(parent__isnull=True))
        rows_ids = [row.id for row in rows]
        return RowsUploader(
            rows=rows,
            cells=Cell.objects.filter(row__in=rows_ids),
            values=Value.objects.none()
        )

    @staticmethod
    def create_document_uploader(sheet: Sheet, document_id: str) -> 'RowsUploader':
        """Создание выгрузчика строк листа с учетом документа.

        Выгружает лист конкретного документа с подстроками и значениями.
        """
        rows = sheet.rowdimension_set.filter(
            Q(parent__isnull=True) | Q(parent__isnull=False, document_id=document_id)
        )
        rows_ids = [row.id for row in rows]
        return RowsUploader(
            rows=rows,
            cells=Cell.objects.filter(row__in=rows_ids),
            values=sheet.value_set.filter(document_id=document_id)
        )

    _rows_fields = (
        'id', 'index', 'height',
        'fixed', 'hidden', 'dynamic',
        'aggregation', 'created_at', 'updated_at',
        'parent_id', 'document_id', 'user',
    )
    _cells_fields = (
        'id', 'kind', 'editable',
        'formula', 'comment', 'default',
        'mask', 'tooltip', 'column_id',
        'row_id', 'horizontal_align', 'vertical_align',
        'size', 'strong', 'italic',
        'strike', 'underline', 'color',
        'background', 'border_style', 'border_color'
    )
    _values_fields = (
        'column_id', 'row_id', 'value', 'verified', 'error'
    )
    _merged_cells_fields = (
        'min_col', 'min_row', 'max_col', 'max_row'
    )

    @staticmethod
    def _upload_raw_data(objects: Union[QuerySet, Sequence[Model]], fields: tuple) -> list[dict]:
        """Выгрузка необработанных данных."""
        if isinstance(objects, QuerySet):
            return list(objects.values(*fields))
        else:
            return [model_to_dict(obj, fields=fields) for obj in objects]

    def _upload_raw_rows(self) -> list[dict]:
        """Выгрузка необработанных строк листа."""
        return self._upload_raw_data(self.rows, self._rows_fields)

    def _upload_raw_cells(self) -> list[dict]:
        """Выгрузка необработанных ячеек листа."""
        return self._upload_raw_data(self.cells, self._cells_fields)

    def _upload_raw_values(self) -> list[dict]:
        """Выгрузка необработанных значений листа."""
        return self._upload_raw_data(self.values, self._values_fields)

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
        for cell in cells:
            default = cell['default']
            del cell['default']
            value = next(
                (value for value in values
                 if value['row_id'] == cell['row_id'] and value['column_id'] == cell['column_id']),
                None
            )
            if value is not None:
                cell.update(value)
            else:
                cell.update({'value': default, 'verified': True, 'error': None})
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
