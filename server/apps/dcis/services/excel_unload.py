import posixpath
from datetime import datetime
from os.path import join

from graphql_relay import from_global_id
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from openpyxl.styles import Border, Side, Alignment, Font
from apps.dcis.models import RowDimension, ColumnDimension, Cell, Sheet, Document, MergedCell
from devind import settings


class DocumentUnload:

    def __init__(self, document_id: str, host: str):
        """Генерация."""
        self.host = host
        document = Document.objects.get(pk=from_global_id(document_id)[1])
        sheets = Sheet.objects.filter(document=document)
        self.rows = RowDimension.objects.filter(sheet_id__in=sheets)
        self.columns = ColumnDimension.objects.filter(sheet_id__in=sheets)
        self.cells = Cell.objects.filter(column_id__in=self.columns, row_id__in=self.rows)
        self.merged_cells = MergedCell.objects.filter(sheet_id__in=sheets)
        self.path: str = join(settings.DOCUMENTS_DIR, f'document_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}')

    def xlsx(self):
        """Генерация выгрузки."""
        workbook: Workbook = Workbook()
        ws = workbook.active
        ws.title = f'Выгрузка документа'
        for cell in self.cells:
            row_position = cell.row.index
            column_position = cell.column.index
            if cell.default is None:
                cell.default = ''
            ws.cell(row_position, column_position, f'{cell.default}').alignment = Alignment(
                vertical=cell.vertical_align,
                horizontal=cell.horizontal_align,
                wrap_text=True
            )
            print(f'{cell.default}')
        for col in self.columns:
            ws.column_dimensions[get_column_letter(col.index)].width = col.width or 20
        for row in self.rows:
            ws.row_dimensions[row.index].height = row.height
        for mc in self.merged_cells:
            ws.merge_cells(
                start_row=mc.min_row,
                start_column=mc.min_col,
                end_row=mc.max_row,
                end_column=mc.max_col
            )
        path_output = f'{self.path}.xlsx'
        workbook.save(path_output)
        return posixpath.relpath(path_output, settings.BASE_DIR)

