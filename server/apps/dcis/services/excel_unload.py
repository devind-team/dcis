import posixpath
from datetime import datetime
from os.path import join

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from apps.dcis.models import Cell, Sheet, Document
from devind import settings


class DocumentUnload:

    def __init__(self, document: Document, host: str):
        """Генерация."""
        self.host = host
        self.sheets = Sheet.objects.filter(document=document)
        self.cells = Cell.objects.all()
        self.path: str = join(settings.DOCUMENTS_DIR, f'document_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}')

    def xlsx(self):
        """Генерация выгрузки."""
        workbook: Workbook = Workbook()
        for sheet in self.sheets:
            ws = workbook.create_sheet(sheet.name, -1)
            rows = sheet.rowdimension_set.all()
            columns = sheet.columndimension_set.all()
            cells = self.cells.filter(row__in=rows, column__in=columns)

            # Вписываем значения в ячейки
            for cell in cells:
                row_position = cell.row.index
                column_position = cell.column.index
                value = cell.default or ''
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
                    color=cell.color
                )
                # Заливка ячейки
                ws.cell(row_position, column_position).fill = PatternFill(bgColor=cell.background)

            # Ширина и высота для колонок и строк соответственно
            for column in columns:
                if column.width:
                    ws.column_dimensions[get_column_letter(column.index)].width = column.width
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
        path_output = f'{self.path}.xlsx'
        workbook.save(path_output)
        return posixpath.relpath(path_output, settings.BASE_DIR)
