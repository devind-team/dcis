# Модуль document_unload_services



## Класс BuildRow

Дата класс содержащий строку и основную информацию о строке.

### Методы

| Сигнатура                                                                                                                                             | Декораторы | Описание            |
| :---------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :------------------ |
| __init__( self, row: apps.dcis.models.sheet.RowDimension, row_add_date: str, row_update_date: str, division_name: str, division_head: str, user: str) | -          | -                   |
| __repr__(self)                                                                                                                                        | -          | Return repr(self).  |
| __eq__(self, other)                                                                                                                                   | -          | Return self==value. |

## Класс BuildCell

Дата класс содержащий собираемую информацию о ячейки.

### Методы

| Сигнатура                                                                                                                                                                                                                                 | Декораторы | Описание            |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :------------------ |
| __init__( self, cell: apps.dcis.models.sheet.Cell, value: str, alignment: openpyxl.styles.alignment.Alignment, font: openpyxl.styles.fonts.Font, border: openpyxl.styles.borders.Border, pattern_fill: openpyxl.styles.fills.PatternFill) | -          | -                   |
| __repr__(self)                                                                                                                                                                                                                            | -          | Return repr(self).  |
| __eq__(self, other)                                                                                                                                                                                                                       | -          | Return self==value. |

## Класс DocumentUnload

Выгрузка документа в формате Excel.

### Методы

| Сигнатура                                                                                                          | Декораторы | Описание                                                                                                                                           |
| :----------------------------------------------------------------------------------------------------------------- | :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| __init__( self, document: apps.dcis.models.document.Document, host: str, additional: list[str], divisions_id=None) | -          | Инициализацияdocument - выгружаемый документhost - текущий хостadditional - дополнительные параметрыdivisions_id - выгружаемые дивизионы в запросе |
| xlsx(self)                                                                                                         | -          | -                                                                                                                                                  |