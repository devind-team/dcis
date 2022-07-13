# Модуль sheet_unload_services



## Класс DataUnloader

Выгрузчик данных.

### Методы

| Сигнатура                                                                                                                                                                                          | Декораторы     | Описание                        |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------- | :------------------------------ |
| unload_data(self) -&#62; list[dict] &#124; dict                                                                                                                                                    | abstractmethod | Выгрузка данных.                |
| unload(self) -&#62; list[dict] &#124; dict                                                                                                                                                         | -              | Выгрузка данных с учетом кеша.  |
| unload_raw_data( cls, objects: Union[django.db.models.query.QuerySet, Sequence[django.db.models.base.Model]], fields: Sequence[str], properties: Optional[Sequence[str]] = None) -&#62; list[dict] | classmethod    | Выгрузка необработанных данных. |

## Класс SheetColumnsUnloader

Выгрузчик колонок листа.

### Методы

| Сигнатура                                                                                                          | Декораторы | Описание                |
| :----------------------------------------------------------------------------------------------------------------- | :--------- | :---------------------- |
| __init__( self, columns: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.ColumnDimension]]) | -          | -                       |
| unload_data(self) -&#62; list[dict] &#124; dict                                                                    | -          | Выгрузка колонок листа. |

## Класс SheetRowsUploader

Выгрузчик строк листа.

### Методы

| Сигнатура                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Декораторы | Описание              |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :-------------------- |
| __init__( self, columns_unloader: apps.dcis.services.sheet_unload_services.SheetColumnsUnloader, rows: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.RowDimension]], cells: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.Cell]], merged_cells: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.MergedCell]], values: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.Value]]) | -          | -                     |
| unload_data(self) -&#62; list[dict] &#124; dict                                                                                                                                                                                                                                                                                                                                                                                                                                | -          | Выгрузка строк листа. |

## Класс SheetPartialRowsUploader

Выгрузчик подмножества строк листа.

### Методы

| Сигнатура                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Декораторы | Описание                        |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------- | :------------------------------ |
| __init__( self, columns_unloader: apps.dcis.services.sheet_unload_services.SheetColumnsUnloader, rows: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.RowDimension]], cells: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.Cell]], merged_cells: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.MergedCell]], values: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.Value]], rows_global_indices_map: dict[dict]) | -          | -                               |
| unload_data(self) -&#62; list[dict] &#124; dict                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | -          | Частичная выгрузка строк листа. |

## Класс SheetUploader

Выгрузчик листа.

### Методы

| Сигнатура                                                                                                                      | Декораторы | Описание        |
| :----------------------------------------------------------------------------------------------------------------------------- | :--------- | :-------------- |
| __init__( self, sheet: apps.dcis.models.document.Sheet, fields: Sequence[str], document_id: int &#124; str &#124; None = None) | -          | -               |
| unload_data(self) -&#62; list[dict] &#124; dict                                                                                | -          | Выгрузка листа. |