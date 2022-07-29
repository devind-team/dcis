import posixpath
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from os.path import join
from typing import Type

from django.conf import settings
from django.db.models import Q
from graphql import ResolveInfo
from graphql_relay import from_global_id
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from apps.core.models import User
from apps.dcis.models import Cell, ColumnDimension, Document, MergedCell, Period, Project, RowDimension, Value
from apps.dcis.permissions import (
    can_view_document,
)


@dataclass
class BuildRow:
    """Дата класс содержащий строку и основную информацию о строке."""
    row: RowDimension
    row_add_date: str
    row_update_date: str
    division_name: str
    division_head: str
    user: str


@dataclass
class BuildCell:
    """Дата класс содержащий собираемую информацию о ячейки."""
    cell: Cell
    value: str
    alignment: Alignment
    font: Font
    border: Border
    pattern_fill: PatternFill


class DocumentUnload:
    """Выгрузка документа в формате Excel."""

    ALLOW_ADDITIONAL: list[str] = ['row_add_date', 'row_update_date', 'division_name', 'division_head', 'user']
    DIVISION_INFO_CACHE: dict[int, tuple[str, str]] = {}

    def __init__(self, document: Document, host: str, additional: list[str], divisions_id=None):
        """Инициализация

            document - выгружаемый документ
            host - текущий хост
            additional - дополнительные параметры
            divisions_id - выгружаемые дивизионы в запросе
        """
        if divisions_id is None:
            divisions_id = []
        self.document: Document = document
        self.period: Period = Period.objects \
            .select_related('project') \
            .get(pk=self.document.period_id)
        self.project: Project = self.period.project
        self.sheets = document.sheets\
            .prefetch_related('columndimension_set', 'mergedcell_set')\
            .all()
        self.host: str = host
        self.additional: list[str] = [field for field in additional if field in self.ALLOW_ADDITIONAL]
        self.divisions_id: list[int] = divisions_id
        self.path: str = join(settings.DOCUMENTS_DIR, f'document_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.xlsx')

    def xlsx(self):
        workbook: Workbook = Workbook()
        workbook.remove(workbook.active)
        for sheet in self.sheets:
            work_sheet = workbook.create_sheet(sheet.name)
            columns: list[ColumnDimension] = sheet.columndimension_set.all()
            rows: list[RowDimension] = sheet.rowdimension_set.filter(
                Q(parent__isnull=True) | Q(
                    document=self.document, parent_id__isnull=False
                )
            )
            rows_id: list[int] = [row.id for row in rows]
            cells: list[Cell] = Cell.objects.filter(row_id__in=rows_id).all()
            values: list[Value] = Value.objects.filter(document=self.document, row_id__in=rows_id).all()
            build_rows: list[BuildRow] = self._build_rows(rows)
            build_cells: dict[str, BuildCell] = self._build_cells(cells, values)
            build_merged_cells: dict[int, list[MergedCell]] = self._build_merge_cells(sheet.mergedcell_set.all())

            # Собираем xlsx файл
            row_index: int = 1
            offset_row: int = 0
            for build_row in build_rows:
                column_index: int = 1
                for column in columns:
                    cell: BuildCell | None = build_cells.get(f'{column.pk}:{build_row.row.pk}')
                    if cell:
                        work_sheet.cell(row_index, column_index, cell.value)
                        work_sheet.cell(row_index, column_index).alignment = cell.alignment
                        work_sheet.cell(row_index, column_index).font = cell.font
                        # Временно отключено
                        # work_sheet.cell(row_index, column_index).border = cell.border
                        # work_sheet.cell(row_index, column_index).fill = cell.pattern_fill
                    column_index += 1
                # Дополнительные колонки
                for ac in self.additional:
                    work_sheet.cell(row_index, column_index, getattr(build_row, ac))
                    column_index += 1
                # Пропускаем объединение, если строка дочерняя
                if build_row.row.parent_id is not None:
                    offset_row += 1

                # Высота строки, если она задана
                if build_row.row.height:
                    work_sheet.row_dimensions[row_index].height = build_row.row.height

                # Объединяем ячейки
                if row_index - offset_row in build_merged_cells:
                    for merge_cell in build_merged_cells[row_index - offset_row]:
                        work_sheet.merge_cells(
                            start_column=merge_cell.min_col,
                            start_row=merge_cell.min_row + offset_row,
                            end_column=merge_cell.max_col,
                            end_row=merge_cell.max_row + offset_row
                        )

                row_index += 1

            for column in columns:
                if column.width:
                    work_sheet.column_dimensions[get_column_letter(column.index)].width = column.width // 7
            for ci in range(len(columns) + 1, len(columns) + len(self.additional) + 1):
                work_sheet.column_dimensions[get_column_letter(ci)].width = 20

        workbook.save(self.path)
        return posixpath.relpath(self.path, settings.BASE_DIR)

    def _build_rows(self, rows: list[RowDimension], parent_id: Type[int] | None = None) -> list[BuildRow]:
        """Функция собирает все строки, включая дочерние в плоский массив."""
        date_format: str = '%H:%M %d.%m.%Y'
        build_rows: list[BuildRow] = []
        current_rows: list[RowDimension] = [row for row in rows if row.parent_id == parent_id]
        for current_row in current_rows:
            division_name, division_head = self._division_info(current_row.user)
            build_row = BuildRow(
                current_row,
                current_row.created_at.strftime(date_format),
                current_row.updated_at.strftime(date_format),
                division_name,
                division_head,
                current_row.user.get_full_name if current_row.user is not None else ''
            )
            build_rows = [*build_rows, build_row, *self._build_rows(rows, current_row.pk)]
        return build_rows

    @staticmethod
    def _build_merge_cells(merged_cells: list[MergedCell]) -> dict[int, list[MergedCell]]:
        build_mc: dict[int, list[MergedCell]] = defaultdict(list)
        for merge_cell in merged_cells:
            build_mc[merge_cell.max_row].append(merge_cell)
        return build_mc

    def _division_info(self, user: User | None) -> tuple[str, str]:
        """Функция возвращает название дивизиона и начальника этого дивизиона.

        Возвращать информацию можно только из моделей для которых указаны поля:
            - user - начальник дивизиона
            - users - список сотрудников дивизиона
        Модель должна содержать:
            - name - название дивизиона
            - code - код дивизиона
         related_name для пользователя должно подчиняться протоколу
            getattr(user, project.content_type.model) -> получаем дивизион, где пользователь начальник
            getattr(user, f'{project.content_type.model}s') -> получаем мой список дивизионов
        """
        if user is None or self.project.content_type.model not in ['department']:
            return '', ''
        if user.id in self.DIVISION_INFO_CACHE:
            return self.DIVISION_INFO_CACHE[user.id]
        divisions = getattr(user, f'{self.project.content_type.model}s').all()
        division_name = ', '.join([f'{division.name} ({division.code})' for division in divisions])
        division_head = ', '.join([division.user.get_full_name for division in divisions if division.user is not None])
        self.DIVISION_INFO_CACHE[user.id] = division_name, division_head,
        return division_name, division_head

    def _build_cells(self, cells: list[Cell], values: list[Value]) -> dict[str, BuildCell]:
        """Собираем ячейки в хеш таблицу для индексации."""
        build_values: dict[str, Value] = {f'{value.column_id}:{value.row_id}': value.value for value in values}
        return {
            f'{cell.column_id}:{cell.row_id}': BuildCell(
                cell,
                build_values.get(f'{cell.column_id}:{cell.row_id}', cell.default),
                self._cell_alignment(cell),
                self._cell_font(cell),
                self._cell_border(cell),
                self._cell_pattern_fill(cell)
            )
            for cell in cells
        }

    @staticmethod
    def _cell_alignment(cell: Cell) -> Alignment:
        return Alignment(
            vertical=cell.vertical_align if cell.vertical_align != 'middle' else 'center',
            horizontal=cell.horizontal_align,
            wrap_text=True
        )

    @staticmethod
    def _cell_font(cell: Cell) -> Font:
        return Font(
            size=cell.size,
            bold=cell.strong,
            italic=cell.italic,
            strike=cell.strike,
            underline=cell.underline,
            color=f'{cell.color[1:]}'
        )

    def _cell_border(self, cell: Cell) -> Border:
        border_styles = {
            position: self._cell_border_side(cell, position)
            for position in ['top', 'bottom', 'left', 'right', 'diagonal']
        }
        return Border(
            diagonalDown=cell.border_style.get('diagonalDown'),
            diagonalUp=cell.border_style.get('diagonalUp'),
            **border_styles
        )

    @staticmethod
    def _cell_pattern_fill(cell: Cell) -> PatternFill:
        return PatternFill(
            fill_type='solid',
            start_color=f'{cell.background[1:]}',
            end_color=f'{cell.background[1:]}'
        )

    @staticmethod
    def _cell_border_side(cell: Cell, position: str) -> Side:
        return Side(
            border_style=cell.border_style.get(position),
            color=f'{cell.border_color[position][1:]}' if cell.border_color[position] else None
        )


def document_upload(info: ResolveInfo, document_id: str, additional: list[str] | None = None) -> str:
    """Функция выгрузки документа."""
    if not additional:
        additional = []
    document = Document.objects.get(pk=from_global_id(document_id)[1])
    can_view_document(info.context.user, document)
    document_unload: DocumentUnload = DocumentUnload(document, info.context.get_host(), additional)
    return document_unload.xlsx()
