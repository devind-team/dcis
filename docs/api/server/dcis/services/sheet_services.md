# Модуль sheet_services



### Функции

| Сигнатура                                                                                                                                                                                                                       | Декораторы         | Описание                                                                                                                                                                |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| rename_sheet( sheet: apps.dcis.models.document.Sheet, name: str) -&#62; tuple[apps.dcis.models.document.Sheet, list[apps.dcis.models.sheet.Cell]]                                                                               | transaction.atomic | Переименование листа с учетом формул.sheet.name -&#62; name:param sheet - лист:param name - новое имя листа                                                             |
| change_column_dimension( column_dimension: apps.dcis.models.sheet.ColumnDimension, width: int &#124; None, fixed: bool, hidden: bool, kind: str) -&#62; apps.dcis.models.sheet.ColumnDimension                                  | -                  | Изменение колонки.                                                                                                                                                      |
| add_row_dimension( user: apps.core.models.User, sheet: apps.dcis.models.document.Sheet, document_id: str &#124; int, parent_id: int &#124; None, index: int, global_index: int, global_indices_map: dict[int, int]) -&#62; dict | transaction.atomic | Добавление строки.После добавления строки, строка приобретает новый индекс,соответственно, все строки после вставленной строки должны увеличить свой индекс на единицу. |
| change_row_dimension( row_dimension: apps.dcis.models.sheet.RowDimension, height: int, fixed: bool, hidden: bool, dynamic: bool) -&#62; apps.dcis.models.sheet.RowDimension                                                     | -                  | Изменение строки.                                                                                                                                                       |
| delete_row_dimension(row_dimension: apps.dcis.models.sheet.RowDimension) -&#62; int                                                                                                                                             | transaction.atomic | Удаление строки.После удаления строки, все строки после удаленной строки должны уменьшить свой индекс на единицу.                                                       |
| change_cells_option( cells: Sequence[apps.dcis.models.sheet.Cell], field: str, value: str &#124; int &#124; bool &#124; None) -&#62; list[dict]                                                                                 | transaction.atomic | Изменение свойств ячеек.                                                                                                                                                |
| move_merged_cells( sheet: apps.dcis.models.document.Sheet, idx: int, offset: int, delete: bool = False) -&#62; None                                                                                                             | -                  | Двигаем объединенные строки в зависимости от добавления или удаления.В будущем метод нужно сделать универсальным (и для колонок).                                       |

## Класс CheckCellOptions

Проверка возможности изменения свойств ячеек.

### Методы

| Сигнатура                                                                                                                                                               | Декораторы | Описание                                                               |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :--------------------------------------------------------------------- |
| __init__()                                                                                                                                                              | -          | -                                                                      |
| __new__( cls, field: str, value: str) -&#62; apps.dcis.services.sheet_services.CheckCellOptions.Success &#124; apps.dcis.services.sheet_services.CheckCellOptions.Error | -          | Create and return a new object. See help(type) for accurate signature. |