from abc import ABC, abstractmethod
from functools import reduce
from itertools import chain
from typing import Optional, Sequence, Union

from django.db.models import Model, Q, QuerySet
from openpyxl.utils import get_column_letter

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

    @classmethod
    def unload_raw_data(
        cls,
        objects: Union[QuerySet, Sequence[Model]],
        fields: tuple,
        properties: Optional[Sequence[str]] = None
    ) -> list[dict]:
        """Выгрузка необработанных данных."""
        if properties is not None:
            result: list[dict] = []
            for obj in (objects.all() if isinstance(objects, QuerySet) else objects):
                obj_dict = cls._model_to_dict(obj, fields=fields)
                for pr in properties:
                    obj_dict[pr] = getattr(obj, pr)
                result.append(obj_dict)
            return result
        if isinstance(objects, QuerySet):
            return list(objects.values(*fields))
        return [cls._model_to_dict(obj, fields=fields) for obj in objects]

    @staticmethod
    def _model_to_dict(instance: Model, fields: Optional[Sequence[str]] = None) -> dict:
        """Преобразование модели в словарь."""
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            if fields is not None and f.name in fields:
                data[f.name] = f.value_from_object(instance)
        return data


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
        columns = self.columns_unloader.unload()
        rows = self._unload_raw_rows()
        cells = self._unload_raw_cells()
        merged_cells = self._unload_raw_merged_cells()
        values = self._unload_raw_values()
        columns_map = self._create_columns_map(columns)
        merged_cells_map = self._create_merged_cells_map(merged_cells)
        merged_cell_positions = self._create_merged_cell_positions(merged_cells)
        row_trees = self._add_row_names(self._connect_rows(rows))
        rows = self._sort_rows(row_trees)
        self._add_cell_values(cells, values)
        self._add_cells(rows, cells)
        self._add_cell_properties(rows, columns_map, merged_cells_map)
        self._prepare_row_cells(rows, merged_cells_map, merged_cell_positions)
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
    _merged_cells_fields = ()
    _merged_cells_properties = (
        'colspan', 'rowspan', 'target', 'cells',
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
        return self.unload_raw_data(self.merged_cells, self._merged_cells_fields, self._merged_cells_properties)

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
    def _add_cell_values(cells: list[dict], values: list[dict]) -> None:
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

    @staticmethod
    def _add_cells(rows: list[dict], cells: list[dict]) -> None:
        """Добавление ячеек к строкам."""
        for row in rows:
            row['cells'] = [cell for cell in cells if cell['row_id'] == row['id']]

    @classmethod
    def _add_cell_properties(cls, rows: list[dict], columns_map: dict[dict], merged_cells_map: dict[dict]) -> None:
        """Добавление свойств к ячейкам."""
        for row in rows:
            for cell in row['cells']:
                column = columns_map[cell['column_id']]
                cls._add_cell_positions(row, column, cell)
                cls._add_cell_spans(row, cell, merged_cells_map)

    @staticmethod
    def _create_columns_map(columns: list[dict]) -> dict[dict]:
        """Создание структуры для быстрого поиска колонок по id."""
        return reduce(lambda a, c: {**a, c['id']: c}, columns, {})

    @staticmethod
    def _create_merged_cells_map(merged_cells: list[dict]) -> dict[dict]:
        """Создание структуры для быстрого поиска объединенных ячеек по позиции основной ячейки."""
        return reduce(lambda a, c: {**a, c['target']: c}, merged_cells, {})

    @staticmethod
    def _create_merged_cell_positions(merged_cells: list[dict]) -> list[str]:
        """Создание списка позиций объединенных строк."""
        return reduce(lambda a, c: [*a, *c['cells']], merged_cells, [])

    @staticmethod
    def _add_cell_positions(row: dict, column: dict, cell: dict) -> None:
        """Добавление позиций для ячейки."""
        letter = get_column_letter(column['index'])
        cell['position'] = f'{letter}{row["name"]}'
        cell['global_position'] = f'{letter}{row["global_index"]}'

    @classmethod
    def _add_cell_spans(cls, row: dict, cell: dict, merged_cells_map: dict) -> None:
        """Добавление объединений по колонкам и строкам для ячейки."""
        root_cell = cls._find_root_cell(row, cell)
        merged_cell = merged_cells_map.get(root_cell['position'], None)
        cell['colspan'] = merged_cell['colspan'] if merged_cell else 1
        cell['rowspan'] = merged_cell['rowspan'] if merged_cell else 1

    @classmethod
    def _prepare_row_cells(cls, rows: list[dict], merged_cells_map: dict, merged_cell_positions: list[str]) -> None:
        """Сортировка ячеек строк с удалением лишних ячеек."""
        for row in rows:
            cells: list[dict] = []
            for cell in row['cells']:
                root_cell = cls._find_root_cell(row, cell)
                if root_cell['position'] in merged_cells_map or root_cell['position'] not in merged_cell_positions:
                    cells.append(cell)
            row['cells'] = sorted(cells, key=lambda c: c['global_position'])

    @classmethod
    def _find_root_cell(cls, row: dict, cell: dict) -> dict:
        """Нахождение корневой ячейки для ячейки дочерней строки.

        Корневой считается ячейка лежащая в той же колонке в строке верхнего уровня.
        """
        if row['parent'] is None:
            return cell
        return cls._find_root_cell(
            row['parent'],
            next(
                parent_cell for parent_cell in row['parent']['cells']
                if parent_cell['column_id'] == cell['column_id']
            )
        )


class SheetUploader(DataUnloader):
    """Выгрузчик листа."""

    def __init__(self, sheet: Sheet, fields: Sequence[str], document_id: Optional[Union[int, str]] = None):
        super().__init__()
        self.sheet = sheet
        self.fields = fields
        self.document_id = document_id

    def unload_data(self) -> Union[list[dict], dict]:
        """Выгрузка листа."""
        sheet = self._model_to_dict(
            self.sheet,
            fields=[field for field in self.fields if field not in ('columns', 'rows')]
        )
        columns_unloader = SheetColumnsUnloader(self.sheet.columndimension_set.all())
        if 'columns' in self.fields:
            sheet['columns'] = columns_unloader.unload()
        if 'rows' in self.fields:
            if self.document_id is not None:
                rows = self.sheet.rowdimension_set.filter(
                    Q(parent__isnull=True) | Q(parent__isnull=False, document_id=self.document_id)
                )
                sheet['rows'] = SheetRowsUploader(
                    columns_unloader=columns_unloader,
                    rows=rows,
                    cells=Cell.objects.filter(row__in=[row.id for row in rows]),
                    merged_cells=self.sheet.mergedcell_set.all(),
                    values=self.sheet.value_set.filter(document_id=self.document_id)
                ).unload()
            else:
                rows = self.sheet.rowdimension_set.filter(parent__isnull=True)
                sheet['rows'] = SheetRowsUploader(
                    columns_unloader=columns_unloader,
                    rows=rows,
                    cells=Cell.objects.filter(row__in=[row.id for row in rows]),
                    merged_cells=self.sheet.mergedcell_set.all(),
                    values=Value.objects.none()
                ).unload()
        return sheet
