# Модуль value_services

Файл, содержащий сервисы для изменения значений ячеек.

### Функции

| Сигнатура                                                                                                                                                                                                                                                                                                                                           | Декораторы | Описание                                                     |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :----------------------------------------------------------- |
| update_or_create_value( document: apps.dcis.models.document.Document, cell: apps.dcis.models.sheet.Cell, sheet_id: int &#124; str, value: str, payload: Any = None) -&#62; apps.dcis.services.value_services.UpdateOrCrateValuesResult                                                                                                              | -          | Создание или обновление значения.                            |
| update_or_create_file_value( user: apps.core.models.User, document_id: int &#124; str, sheet_id: int &#124; str, column_id: int &#124; str, row_id: int &#124; str, value: str, remaining_files: list[int], new_files: list[django.core.files.uploadedfile.InMemoryUploadedFile]) -&#62; apps.dcis.services.value_services.UpdateOrCrateValueResult | -          | Изменение файлов значения ячейки типа `Файл`.                |
| create_file_value_archive(value: apps.dcis.models.sheet.Value, name: str) -&#62; str                                                                                                                                                                                                                                                                | -          | Создание архива значения ячейки типа `Файл`.                 |
| get_file_value_files(value: apps.dcis.models.sheet.Value) -&#62; list[devind_core.models.File]                                                                                                                                                                                                                                                      | -          | Получение файлов значения ячейки типа `Файл`.                |
| get_file_value_payload(value: apps.dcis.models.sheet.Value) -&#62; list[int]                                                                                                                                                                                                                                                                        | -          | Получение дополнительных данных значения ячейки типа `Файл`. |

## Класс UpdateOrCrateValueResult

Результат создания или обновления значения.

### Методы

| Сигнатура                                                                                          | Декораторы | Описание                                                                    |
| :------------------------------------------------------------------------------------------------- | :--------- | :-------------------------------------------------------------------------- |
| __init__( _cls, value: apps.dcis.models.sheet.Value, updated_at: datetime.datetime, created: bool) | -          | Create new instance of UpdateOrCrateValueResult(value, updated_at, created) |
| __new__( _cls, value: apps.dcis.models.sheet.Value, updated_at: datetime.datetime, created: bool)  | -          | Create new instance of UpdateOrCrateValueResult(value, updated_at, created) |
| __repr__(self)                                                                                     | -          | Return a nicely formatted representation string                             |
| __getnewargs__(self)                                                                               | -          | Return self as a plain tuple. Used by copy and pickle.                      |

## Класс UpdateOrCrateValuesResult

Результат создания или обновления значения.

### Методы

| Сигнатура                                                                                  | Декораторы | Описание                                                             |
| :----------------------------------------------------------------------------------------- | :--------- | :------------------------------------------------------------------- |
| __init__( _cls, values: list[apps.dcis.models.sheet.Value], updated_at: datetime.datetime) | -          | Create new instance of UpdateOrCrateValuesResult(values, updated_at) |
| __new__( _cls, values: list[apps.dcis.models.sheet.Value], updated_at: datetime.datetime)  | -          | Create new instance of UpdateOrCrateValuesResult(values, updated_at) |
| __repr__(self)                                                                             | -          | Return a nicely formatted representation string                      |
| __getnewargs__(self)                                                                       | -          | Return self as a plain tuple. Used by copy and pickle.               |