# Модуль sheet_unload_services

Описание модуля

# Класс DataUnloader

Описание класса Выгрузчик данных.

## Методы

| Signature                                                                                                                                                                                      | Decorator           | Docstring                       |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ | :------------------------------ |
| unload_data(self) -> Union[list[dict], dict]                                                                                                                                                   | ['@abstractmethod'] | Выгрузка данных.                |
| unload(self) -> Union[list[dict], dict]                                                                                                                                                        | -                   | Выгрузка данных с учетом кеша.  |
| unload_raw_data( cls, objects: Union[django.db.models.query.QuerySet, Sequence[django.db.models.base.Model]], fields: Sequence[str], properties: Optional[Sequence[str]] = None) -> list[dict] | ['@classmethod']    | Выгрузка необработанных данных. |

# Класс SheetColumnsUnloader

Описание класса Выгрузчик колонок листа.

## Методы

| Signature                                                                                                          | Decorator | Docstring               |
| :----------------------------------------------------------------------------------------------------------------- | :-------- | :---------------------- |
| __init__( self, columns: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.ColumnDimension]]) | -         |                         |
| unload_data(self) -> Union[list[dict], dict]                                                                       | -         | Выгрузка колонок листа. |

# Класс SheetRowsUploader

Описание класса Выгрузчик строк листа.

## Методы

| Signature                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Decorator | Docstring             |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- | :-------------------- |
| __init__( self, columns_unloader: apps.dcis.services.sheet_unload_services.SheetColumnsUnloader, rows: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.RowDimension]], cells: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.Cell]], merged_cells: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.MergedCell]], values: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.Value]]) | -         |                       |
| unload_data(self) -> Union[list[dict], dict]                                                                                                                                                                                                                                                                                                                                                                                                                                   | -         | Выгрузка строк листа. |

# Класс SheetPartialRowsUploader

Описание класса Выгрузчик подмножества строк листа.

## Методы

| Signature                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Decorator | Docstring                       |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------- | :------------------------------ |
| __init__( self, columns_unloader: apps.dcis.services.sheet_unload_services.SheetColumnsUnloader, rows: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.RowDimension]], cells: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.Cell]], merged_cells: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.MergedCell]], values: Union[django.db.models.query.QuerySet, Sequence[apps.dcis.models.sheet.Value]], rows_global_indices_map: dict[dict]) | -         |                                 |
| unload_data(self) -> Union[list[dict], dict]                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | -         | Частичная выгрузка строк листа. |

# Класс SheetUploader

Описание класса Выгрузчик листа.

## Методы

| Signature                                                                                                                     | Decorator | Docstring       |
| :---------------------------------------------------------------------------------------------------------------------------- | :-------- | :-------------- |
| __init__( self, sheet: apps.dcis.models.document.Sheet, fields: Sequence[str], document_id: Union[int, str, NoneType] = None) | -         |                 |
| unload_data(self) -> Union[list[dict], dict]                                                                                  | -         | Выгрузка листа. |