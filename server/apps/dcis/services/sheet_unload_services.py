from abc import ABC, abstractmethod
from typing import Optional, Sequence, Union

from django.db.models import Model, Q, QuerySet
from django.forms.models import model_to_dict

from apps.dcis.models.sheet import Cell, ColumnDimension, MergedCell, RowDimension, Sheet, Value


class DataUnloader(ABC):
    """Выгрузчик данных."""

    def __init__(self) -> None:
        self.data: Optional[Union[list[dict], dict]] = None

    @abstractmethod
    def unload_data(self) -> Union[list[dict], dict]:
        """Выгрузка данных."""
        ...

    def unload(self) -> Union[list[dict], dict]:
        """Выгрузка данных с учетом кеша."""
        if self.data is not None:
            return self.data
        self.data = self.unload_data()
        return self.data

    @staticmethod
    def unload_raw_data(objects: Union[QuerySet, Sequence[Model]], fields: tuple) -> list[dict]:
        """Выгрузка необработанных данных."""
        if isinstance(objects, QuerySet):
            return list(objects.values(*fields))
        else:
            return [model_to_dict(obj, fields=fields) for obj in objects]


class SheetColumnsUnloader(DataUnloader):
    """Выгрузчик колонок листа."""

    def __init__(self, columns: Union[QuerySet[ColumnDimension], Sequence[ColumnDimension]]) -> None:
        super().__init__()
        self.columns = columns

    def unload_data(self) -> Union[list[dict], dict]:
        """Выгрузка колонок листа."""
        return self.unload_raw_data(self.columns, self._column_fields)

    _column_fields = (
        'id', 'index', 'width',
        'fixed', 'hidden', 'kind',
        'user'
    )


class SheetRowsUploader(DataUnloader):
    """Выгрузчик строк листа."""

    def __init__(
        self,
        columns_unloader: SheetColumnsUnloader,
        rows: Union[QuerySet[RowDimension], Sequence[RowDimension]],
        cells: Union[QuerySet[Cell], Sequence[Cell]],
        merged_cells: Union[QuerySet[MergedCell], Sequence[MergedCell]],
        values: Union[QuerySet[Value], Sequence[Value]]
    ) -> None:
        super().__init__()
        self.columns_unloader = columns_unloader
        self.rows = rows
        self.cells = cells
        self.merged_cells = merged_cells
        self.values = values

    def unload_data(self) -> Union[list[dict], dict]:
        """Выгрузка строк листа."""
        raw_rows = self._unload_raw_rows()
        raw_cells = self._unload_raw_cells()
        raw_values = self._unload_raw_values()
        row_trees = self._add_row_names(self._connect_rows(raw_rows))
        sorted_rows = self._sort_rows(row_trees)
        cells = self._add_cell_values(raw_cells, raw_values)
        rows = self._add_cells(sorted_rows, cells)
        return rows

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
        'background', 'border_style', 'border_color',
    )
    _values_fields = (
        'column_id', 'row_id', 'value', 'verified', 'error',
    )
    _merged_cells_fields = (
        'min_col', 'min_row', 'max_col', 'max_row',
    )

    def _unload_raw_rows(self) -> list[dict]:
        """Выгрузка необработанных строк листа."""
        return self.unload_raw_data(self.rows, self._rows_fields)

    def _unload_raw_cells(self) -> list[dict]:
        """Выгрузка необработанных ячеек листа."""
        return self.unload_raw_data(self.cells, self._cells_fields)

    def _unload_raw_values(self) -> list[dict]:
        """Выгрузка необработанных значений листа."""
        return self.unload_raw_data(self.values, self._values_fields)

    def _unload_raw_merged_cells(self) -> list[dict]:
        """Выгрузка необработанных объединенных ячеек."""
        return self.unload_raw_data(self.merged_cells, self._merged_cells_fields)

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


class SheetUploader(DataUnloader):
    """Выгрузчик листа."""

    def __init__(self, sheet: Sheet, fields: Sequence[str], document_id: Optional[Union[int, str]] = None):
        super().__init__()
        self.sheet = sheet
        self.fields = fields
        self.document_id = document_id

    def unload_data(self) -> Union[list[dict], dict]:
        """Выгрузка листа."""
        sheet = model_to_dict(
            self.sheet,
            fields=[field for field in self.fields if field not in ('columns', 'rows')]
        )
        columns_unloader = SheetColumnsUnloader(self.sheet.columndimension_set.all())
        if 'columns' in self.fields:
            sheet['columns'] = columns_unloader.unload()
        if 'rows' in self.fields:
            if self.document_id is not None:
                rows = sheet.rowdimension_set.filter(parent__isnull=True)
                sheet['rows'] = SheetRowsUploader(
                    columns_unloader=columns_unloader,
                    rows=rows,
                    cells=Cell.objects.filter(row__in=[row.id for row in rows]),
                    merged_cells=sheet.mergedcell_set.all(),
                    values=Value.objects.none()
                ).unload()
            else:
                rows = sheet.rowdimension_set.filter(
                    Q(parent__isnull=True) | Q(parent__isnull=False, document_id=self.document_id)
                )
                sheet['rows'] = SheetRowsUploader(
                    columns_unloader=columns_unloader,
                    rows=rows,
                    cells=Cell.objects.filter(row__in=[row.id for row in rows]),
                    merged_cells=sheet.mergedcell_set.all(),
                    values=sheet.value_set.filter(document_id=self.document_id)
                ).unload()
        return sheet
