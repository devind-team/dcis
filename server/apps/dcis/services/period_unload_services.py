"""Модуль, отвечающий за выгрузку периода."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

from devind_dictionaries.models import Organization
from django.conf import settings
from django.db.models import QuerySet
from openpyxl.cell.cell import VALID_TYPES
from openpyxl.utils import get_column_letter
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from apps.core.models import User
from apps.dcis.helpers.exceptions import is_raises
from apps.dcis.models import Cell, Document, MergedCell, Period, Sheet, Value
from apps.dcis.models.sheet import KindCell
from apps.dcis.permissions import can_view_period_result


@dataclass
class CellData:
    """Данные ячейки."""
    value: str
    data_type: str = 's'
    number_format: str = None


@dataclass
class DataSource:
    """Источник данных для ячейки."""
    organization: Organization
    document: Document | None
    cells: list[CellData]


@dataclass
class Column:
    """Выгружаемый столбец."""
    get_cell: Callable[[DataSource], CellData]
    names: list[str]


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

    def __init__(
        self,
        period: Period,
        organization_ids: list[int],
        status_ids: list[int],
        unload_without_document: bool,
        apply_number_format: bool,
        unload_heads: bool,
        unload_children: bool,
        empty_cell: str
    ) -> None:
        """Инициализация.
        - period - выгружаемый период
        - organization_ids - фильтрация по идентификаторам организаций
        - status_ids - фильтрация по идентификаторам статусов
        - unload_without_document - выгружать организации без документов
        - apply_number_format - применять числовой формат
        - unload_heads - выгружать листы для головных учреждений
        - unload_children - выгружать листы для филиалов
        - empty_cell - строка в пустой ячейке
        """
        self.period = period
        self.path = Path(settings.DOCUMENTS_DIR, f'document_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.xlsx')
        self._organizations = Organization.objects.filter(
            id__in=self.period.division_set.values_list('object_id', flat=True)
        )
        if len(organization_ids):
            self._organizations = self._organizations.filter(id__in=organization_ids)
        self._status_ids = status_ids
        self._unload_without_document = unload_without_document
        self._apply_number_format = apply_number_format
        if unload_heads and unload_children:
            self._sheets = self.period.sheet_set.all()
        else:
            self._sheets = self.period.sheet_set.filter(show_head=unload_heads, show_child=unload_children)
        self._empty_cell = empty_cell
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
        for sheet in self._sheets:
            worksheet = workbook.create_sheet(sheet.name)
            cells = self._get_cells(sheet)
            cell_groups = self._get_cell_groups(sheet, cells)
            columns = self._build_columns(cell_groups)
            self._save_columns(worksheet, columns)
            self._save_rows(worksheet, sheet, columns, cell_groups)
        workbook.save(self.path)
        return f'/{self.path.relative_to(settings.BASE_DIR)}'

    @staticmethod
    def _save_columns(worksheet: Worksheet, columns: list[Column]) -> None:
        """Сохранение название столбцов на лист Excel."""
        max_row_count = max(len(column.names) for column in columns)
        for column_index, column in enumerate(columns, 1):
            for row_index, name in enumerate(column.names, max_row_count - len(column.names) + 1):
                worksheet.cell(row=row_index, column=column_index, value=name)

    def _save_rows(self, worksheet: Worksheet, sheet: Sheet, columns: list[Column], cell_groups: CellGroups) -> None:
        """Сохранение строки на лист Excel."""
        row_index = self._get_header_size(columns) + 1
        values = Value.objects.filter(sheet=sheet)
        for organization in self._get_organizations(sheet):
            document = self.documents_map[organization.id]
            data_source = DataSource(
                organization=organization,
                document=document,
                cells=self._get_cells_data(cell_groups.value_cells, values, document)
            )
            for column_index, column in enumerate(columns, 1):
                cell_data = column.get_cell(data_source)
                cell = worksheet.cell(row=row_index, column=column_index, value=cell_data.value)
                cell.data_type = cell_data.data_type
                if self._apply_number_format and cell_data.number_format:
                    cell.number_format = cell_data.number_format
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

    @classmethod
    def _build_columns(cls, cell_groups: CellGroups) -> list[Column]:
        """Построение столбцов."""
        return [
            *cls._build_left_columns(),
            *cls._build_data_columns(cell_groups),
            *cls._build_right_columns()
        ]

    @staticmethod
    def _build_left_columns() -> list[Column]:
        """Получение столбцов слева от данных."""
        return [
            Column(
                get_cell=lambda s: CellData(s.organization.attributes['idlistedu'], KindCell.NUMERIC),
                names=['IdListEdu'],
            ),
            Column(
                get_cell=lambda s: CellData(s.organization.parent.attributes['idlistedu']
                if s.organization.parent else '', KindCell.NUMERIC),
                names=['id_parent'],
            ),
            Column(get_cell=lambda s: CellData(s.organization.kodbuhg, KindCell.NUMERIC), names=['Бухкод']),
            Column(
                get_cell=lambda s: CellData(
                    s.organization.region.common_id if s.organization.region else '',
                    KindCell.NUMERIC
                ),
                names=['Код региона'],
            ),
            Column(
                get_cell=lambda s: CellData(s.organization.region.name if s.organization.region else ''),
                names=['Регион'],
            ),
            Column(get_cell=lambda s: CellData(s.organization.name), names=['Название учреждения']),
            Column(
                get_cell=lambda s: CellData(s.organization.parent.name if s.organization.parent else ''),
                names=['Название головного учреждения'],
            ),
            Column(
                get_cell=lambda s: CellData(s.document.last_status.status.name
                if s.document and s.document.last_status else ''),
                names=['Статус документа'],
            ),
            Column(get_cell=lambda s: CellData(s.organization.attributes['org_type']), names=['Тип организации']),
        ]

    @classmethod
    def _build_data_columns(cls, cell_groups: CellGroups) -> list[Column]:
        """Получение столбцов с данными."""
        min_column_index = min((hc.cell.column.index for hc in cell_groups.column_header_cells), default=0)
        max_column_index = max(
            (hc.cell.column.index if hc.merged_cell is None else hc.merged_cell.max_col
            for hc in cell_groups.column_header_cells),
            default=0,
        )
        columns: list[Column] = []
        if min_column_index != 0 or max_column_index != 0:
            for column_start_index, column_index in enumerate(range(min_column_index, max_column_index + 1)):
                for cell_index, cell in enumerate(cell_groups.row_header_cells):
                    i = column_start_index * len(cell_groups.row_header_cells) + cell_index
                    columns.append(Column(get_cell=cls._make_get_cell(i), names=[cell.default_error or cell.default]))
        else:
            for i, cell in enumerate(cell_groups.row_header_cells):
                columns.append(Column(get_cell=cls._make_get_cell(i), names=[cell.default_error or cell.default]))
        return columns

    @classmethod
    def _build_right_columns(cls) -> list[Column]:
        """Получение столбцов справа от данных."""
        return [
            Column(
                get_cell=lambda s: CellData(cls._format_datatime(s.document.updated_at) if s.document else ''),
                names=['Дата последнего редактирования']
            ),
            Column(
                get_cell=lambda s: CellData(
                    cls._format_user(s.document.updated_by)
                    if s.document and s.document.updated_by else ''
                ),
                names=['Пользователь'],
            ),
        ]

    def _get_organizations(self, sheet: Sheet) -> list[Organization]:
        """Получение организаций с фильтрацией."""
        result: list[Organization] = []
        parent_filter: dict[str, bool] = {}
        if sheet.show_head and not sheet.show_child:
            parent_filter['parent__isnull'] = True
        elif not sheet.show_head and sheet.show_child:
            parent_filter['parent__isnull'] = False
        for organization in self._organizations.filter(**parent_filter):
            document = self.documents_map[organization.id]
            if (
                self._unload_without_document and
                document is None
            ) or not len(self._status_ids) or (
                document.last_status and document.last_status.status.id in self._status_ids
            ):
                result.append(organization)
        return result

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

    def _get_cells_data(self, cells: list[Cell], values: QuerySet[Value], document: Document) -> list[CellData]:
        """Получение данных для ячеек."""
        result: list[CellData] = []
        for cell in sorted(cells, key=lambda c: [c.column.index, c.row.index]):
            val = self._empty_cell
            for value in values:
                if value.document == document and value.column == cell.column and value.row == cell.row:
                    val = value.value
            data_type = cell.kind
            if data_type not in VALID_TYPES:
                data_type = KindCell.STRING
            if data_type == KindCell.FORMULA:
                if self._is_numeric(val):
                    data_type = KindCell.NUMERIC
                else:
                    data_type = KindCell.STRING
            result.append(CellData(value=val, data_type=data_type, number_format=cell.number_format))
        return result

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
        column_header_index, row_header_index = cls._cut_excess_headers(value_cells, header_cells)
        column_header_cells: list[HeaderCell] = [hc for hc in header_cells if hc.cell.column.index > row_header_index]
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
    def _cut_excess_headers(cls, value_cells: list[Cell], header_cells: list[HeaderCell]) -> tuple[int, int]:
        """Отрезание лишних ячеек от ячеек с данными."""
        value_cells_copy: list[Cell] = [*value_cells]
        value_cells.clear()
        row, column = max(c.row.index for c in value_cells_copy), max(c.column.index for c in value_cells_copy)
        row_size, column_size = 0, 0
        while row > 0 and column > 0:
            row_cells = [c for c in value_cells_copy if c.row.index == row and c.column.index >= column]
            column_cells = [c for c in value_cells_copy if c.column.index == column and c.row.index >= row]
            if len(row_cells) == row_size + 1 and len(column_cells) == column_size + 1:
                value_cells.extend(row_cells)
                value_cells.extend([c for c in column_cells if c.row.index != row or c.column.index != column])
                row, column = row - 1, column - 1
                row_size, column_size = row_size + 1, column_size + 1
            elif len(row_cells) == row_size + 1 or len(row_cells) == row_size and next(
                (c for c in row_cells if c.column.index == column),
                None
            ) is None:
                value_cells.extend([c for c in row_cells if c.row.index != row or c.column.index != column])
                row -= 1
                column_size += 1
            elif len(column_cells) == column_size + 1 or len(column_cells) == column_size and next(
                (c for c in column_cells if c.row.index == row),
                None
            ) is None:
                value_cells.extend([c for c in column_cells if c.row.index != row or c.column.index != column])
                column -= 1
                row_size += 1
            else:
                break
        for cell in set(value_cells_copy) - set(value_cells):
            header_cells.append(HeaderCell(cell=cell, merged_cell=None))
        return row, column

    @staticmethod
    def _make_get_cell(i: int) -> Callable[[DataSource], CellData]:
        """Создание функции для получения значения."""
        def get_cell(s: DataSource) -> CellData:
            return s.cells[i]
        return get_cell

    @staticmethod
    def _format_datatime(datatime: datetime) -> str:
        """Форматирование даты."""
        return f'{datatime:%d.%m.%Y %H:%M}'

    @staticmethod
    def _format_user(user: User) -> str:
        """Форматирование пользователя."""
        result = f'{user.last_name} {user.first_name}'
        if user.sir_name:
            return f'{result} {user.sir_name}'
        return result

    @staticmethod
    def _is_numeric(value: str) -> bool:
        """Является ли значение типом `KindCell.NUMERIC`"""
        return not is_raises(ValueError, lambda: int(value) or float(value))


def unload_period(
    user: User,
    period: Period,
    organization_ids: list[int],
    status_ids: list[int],
    unload_without_document: bool,
    apply_number_format: bool,
    unload_heads: bool,
    unload_children: bool,
    empty_cell: str
) -> str:
    """Выгрузка периода в формате Excel."""
    can_view_period_result(user, period)
    return PeriodUnload(
        period=period,
        organization_ids=organization_ids,
        status_ids=status_ids,
        unload_without_document=unload_without_document,
        apply_number_format=apply_number_format,
        unload_heads=unload_heads,
        unload_children=unload_children,
        empty_cell=empty_cell,
    ).unload()
