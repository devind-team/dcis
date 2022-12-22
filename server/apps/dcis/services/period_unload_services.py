"""Модуль, отвечающий за выгрузку периода."""

from dataclasses import dataclass
from datetime import datetime
from itertools import chain
from pathlib import Path
from typing import Callable

from devind_dictionaries.models import Organization
from django.conf import settings
from django.db.models import QuerySet
from openpyxl.utils import get_column_letter
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from apps.core.models import User
from apps.dcis.models import Cell, Document, MergedCell, Period, Sheet
from apps.dcis.permissions import can_view_period_result


@dataclass
class Column:
    """Выгружаемый столбец."""
    key: str
    names: list[str]


@dataclass
class DataSource:
    """Источник данных для ячейки."""
    organization: Organization
    document: Document | None
    sheet: dict[str, str]


@dataclass
class HeaderCell:
    """Ячейка в шапке таблицы."""
    cell: Cell
    merged_cell: MergedCell | None


@dataclass
class CellGroups:
    """Группы ячеек.
    - value_cells - крайняя правая прямоугольная группа ячеек без readonly и объединенных ячеек
    - column_header_cell - ячейки в шапке таблицы
    - row_header_cells - столбец примыкающий слева к value_cells
    """
    value_cells: list[Cell]
    column_header_cells: list[HeaderCell]
    row_header_cells: list[Cell]


class PeriodUnload:
    """Выгрузка периода в формате Excel."""

    def __init__(self, period: Period) -> None:
        """Инициализация.
        - period - выгружаемы период
        """
        self.period = period
        self.path = Path(settings.DOCUMENTS_DIR, f'document_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.xlsx')
        self._organizations = Organization.objects.filter(
            id__in=self.period.division_set.values_list('object_id', flat=True)
        )
        self._documents = Document.objects.filter(
            period=self.period,
            object_id__in=self._organizations.values_list('id', flat=True)
        )
        self._documents_map: dict[int, Document | None] | None = None

    @property
    def documents_map(self) -> dict[int, Document | None]:
        """Отображение идентификаторов организаций на документы."""
        if self._documents_map is None:
            self._documents_map = self._build_documents_map()
        return self._documents_map

    def unload(self) -> str:
        """Выгрузка."""
        workbook = Workbook()
        workbook.remove(workbook.active)
        for sheet in self.period.sheet_set.all():
            worksheet = workbook.create_sheet(sheet.name)
            cells = self._get_cells(sheet)
            cell_groups = self._get_cell_groups(sheet, cells)
            columns = self._build_columns(cell_groups)
            self._save_columns(worksheet, columns)
            self._save_rows(worksheet, columns)
        workbook.save(self.path)
        return f'/{self.path.relative_to(settings.BASE_DIR)}'

    @staticmethod
    def _save_columns(worksheet: Worksheet, columns: list[Column]) -> None:
        """Сохранение название столбцов на лист Excel."""
        for column_index, column in enumerate(columns, 1):
            for row_index, name in enumerate(column.names, 1):
                worksheet.cell(row=row_index, column=column_index, value=name)

    def _save_rows(self, worksheet: Worksheet, columns: list[Column]) -> None:
        """Сохранение строки на лист Excel."""
        row_index = self._get_header_size(columns) + 1
        for organization in self._organizations:
            document = self.documents_map[organization.id]
            data_source = DataSource(organization=organization, document=document, sheet={})
            for column_index, column in enumerate(columns, 1):
                worksheet.cell(row=row_index, column=column_index, value=self._get_from_source(data_source, column))
            row_index += 1

    def _build_documents_map(self) -> dict[int, Document | None]:
        """Отображение идентификаторов организаций на документы."""
        result: dict[int, Document | None] = {}
        for organization in self._organizations:
            result[organization.id] = next(
                (document for document in self._documents if organization.id == document.object_id),
                None
            )
        return result

    @staticmethod
    def _build_columns(cell_groups: CellGroups) -> list[Column]:
        """Построение столбцов."""
        columns = [
            Column(key='organization.attributes.idlistedu', names=['IdListEdu']),
            Column(key='organization.parent.attributes.idlistedu', names=['id_parent']),
            Column(key='organization.kodbuhg', names=['Бухкод']),
            Column(key='organization.region.common_id', names=['Код региона']),
            Column(key='organization.region.name', names=['Регион']),
            Column(key='organization.name', names=['Название учреждения']),
            Column(key='organization.parent.name', names=['Название головного учреждения']),
            Column(key='document.last_status.status.name', names=['Статус документа']),
            Column(key='organization.kind', names=['Тип организации']),
        ]
        for cell in cell_groups.row_header_cells:
            columns.append(Column(key='organization.kodbuhg', names=[f'{get_column_letter(cell.column.index)}{cell.row.index}']))
        return columns

    @staticmethod
    def _get_header_size(columns: list[Column]) -> int:
        """Размер шапки таблицы."""
        return max(len(column.names) for column in columns)

    @staticmethod
    def _get_cells(sheet: Sheet) -> QuerySet[Cell]:
        """Получение ячеек листа."""
        return Cell.objects.filter(
            row__sheet=sheet,
            row__parent__isnull=True
        ).order_by('row__index', 'column__index')

    @staticmethod
    def _get_merged_cells(sheet: Sheet) -> QuerySet[MergedCell]:
        """Получение объединенных ячеек листа."""
        return MergedCell.objects.filter(sheet=sheet)

    @classmethod
    def _get_cell_groups(cls, sheet: Sheet, cells: QuerySet[Cell]) -> CellGroups:
        """Получение групп ячеек."""
        header_cells: list[HeaderCell] = []
        value_cells: list[Cell] = []
        merged_cells = cls._get_merged_cells(sheet)
        merged_cells_columns: set[int] = set()
        merged_cells_rows: set[int] = set()
        for cell in cells:
            position = f'{get_column_letter(cell.column.index)}{cell.row.index}'
            merged_cell = next((mc for mc in merged_cells if position in mc.cells or position == mc.target), None)
            if not cell.editable:
                header_cells.append(HeaderCell(cell=cell, merged_cell=None))
            elif merged_cell is not None:
                merged_cells_columns.update({*range(merged_cell.min_col, merged_cell.max_col + 1)})
                merged_cells_rows.update({*range(merged_cell.min_row, merged_cell.max_row + 1)})
                if merged_cell.target == position:
                    header_cells.append(HeaderCell(cell=cell, merged_cell=merged_cell))
            else:
                value_cells.append(cell)
        value_cells_copy = [*value_cells]
        value_cells = []
        for cell in value_cells_copy:
            if cell.column.index in merged_cells_columns and cell.row.index in merged_cells_rows:
                header_cells.append(HeaderCell(cell=cell, merged_cell=None))
            else:
                value_cells.append(cell)
        return cls._normalize_cell_groups(value_cells, header_cells)

    @classmethod
    def _normalize_cell_groups(cls, value_cells: list[Cell], header_cells: list[HeaderCell]) -> CellGroups:
        """Нормализация групп ячеек."""
        column_header_index = cls._cut_dimension(value_cells, header_cells, lambda cell: cell.row.index)
        row_header_index = cls._cut_dimension(value_cells, header_cells, lambda cell: cell.column.index)
        column_header_cells: list[HeaderCell] = []
        row_header_cells: list[Cell] = [
            hc.cell for hc in header_cells
            if hc.cell.column.index == row_header_index and hc.cell.row.index > column_header_index
        ]
        return CellGroups(
            value_cells=value_cells,
            column_header_cells=column_header_cells,
            row_header_cells=row_header_cells
        )

    @classmethod
    def _cut_dimension(
        cls,
        value_cells: list[Cell],
        header_cells: list[HeaderCell],
        get_index: Callable[[Cell], int]
    ) -> int:
        """Отрезание лишних элементов по измерению."""
        indices = sorted(set(map(get_index, value_cells)))
        header_index = cls._get_header_index(indices)
        value_cells_copy = [*value_cells]
        value_cells.clear()
        for cell in value_cells_copy:
            if get_index(cell) > header_index:
                value_cells.append(cell)
            elif get_index(cell) == header_index:
                header_cells.append(HeaderCell(cell=cell, merged_cell=None))
        return header_index

    @staticmethod
    def _get_header_index(indices: list[int]) -> int:
        """Получение индекса столбца с заголовками."""
        for current, previous in zip(reversed(indices), chain([indices[-1]], reversed(indices))):
            if previous - current > 1:
                return previous - 1
        return max(indices[0] - 1, 1)

    @staticmethod
    def _get_from_source(data_source: DataSource, column: Column) -> str:
        """Извлечение данных из источника."""
        value = data_source
        for key in column.key.split('.'):
            if value is None:
                return ''
            value = value[key] if isinstance(value, dict) else getattr(value, key)
        return value or ''

def unload_period(user: User, period: Period) -> str:
    """Выгрузка периода в формате Excel."""
    can_view_period_result(user, period)
    return PeriodUnload(period).unload()
