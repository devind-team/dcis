import posixpath
from datetime import datetime
from os.path import join

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.styles.colors import WHITE
from openpyxl.utils import get_column_letter

from apps.dcis.models import Cell, Document
from devind import settings


class DocumentUnload:
    """Выгрузка документа в формате эксель."""

    def __init__(self, document: Document, host: str):
        """Генерация."""
        self.document = document
        self.sheets = document.sheets.all()
        self.host = host
        self.path: str = join(settings.DOCUMENTS_DIR, f'document_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.xlsx')

    def xlsx(self):
        """Генерация выгрузки."""
        workbook: Workbook = Workbook()
        for sheet in self.sheets:
            ws = workbook.create_sheet(sheet.name, -1)
            columns = sheet.columndimension_set.all()
            rows = sheet.rowdimension_set.all()
            cells = Cell.objects.filter(column__in=columns).prefetch_related('row', 'column').all()
            values = sheet.value_set.filter(document=self.document).all()
            build_values = {}
            for build_value in values:
                key = f'{build_value.column_id}:{build_value.row_id}'
                build_values[key] = build_value.value
            # Вписываем значения в ячейки
            for cell in cells:
                row_position = cell.row.index
                column_position = cell.column.index
                value = build_values.get(f'{cell.column_id}:{cell.row_id}', cell.default or '')
                ws.cell(row_position, column_position, f'{value}').alignment = Alignment(
                    vertical=cell.vertical_align,
                    horizontal=cell.horizontal_align,
                    wrap_text=True
                )
                # Стили шрифта ячеек
                ws.cell(row_position, column_position).font = Font(
                    size=cell.size,
                    bold=cell.strong,
                    italic=cell.italic,
                    strike=cell.strike,
                    underline=cell.underline,
                    color=f'{cell.color[1:]}'
                )
                if cell.border_style:
                    border_styles = {position: self._get_border_side(cell, position) for position in ['top', 'bottom', 'left', 'right', 'diagonal']}
                    ws.cell(row_position, column_position).border = Border(
                        diagonalDown=cell.border_style.get('diagonalDown'),
                        diagonalUp=cell.border_style.get('diagonalUp'),
                        **border_styles
                    )
                # Заливка ячейки
                if cell.background != '#FFFFFF' and cell.background != '#FFFFFFFF' and cell.background != WHITE:
                    ws.cell(row_position, column_position).fill = PatternFill(
                        fill_type='solid',
                        start_color=f'{cell.background[1:]}',
                        end_color=f'{cell.background[1:]}'
                    )
            # Ширина и высота для колонок и строк соответственно
            for column in columns:
                if column.width:
                    ws.column_dimensions[get_column_letter(column.index)].width = column.width // 7
            for row in rows:
                if row.height:
                    ws.row_dimensions[row.index].height = row.height

            # Объединение ячеек
            for mc in sheet.mergedcell_set.all():
                ws.merge_cells(
                    start_row=mc.min_row,
                    start_column=mc.min_col,
                    end_row=mc.max_row,
                    end_column=mc.max_col
                )
        workbook.save(self.path)
        return posixpath.relpath(self.path, settings.BASE_DIR)

    @staticmethod
    def _get_border_side(cell: Cell, position: str) -> Side:
        return Side(
            border_style=cell.border_style.get(position),
            color=f'{cell.border_color[position][1:]}' if cell.border_color[position] else None
        )
