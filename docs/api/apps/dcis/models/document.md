# Модуль document

Описание модуля

# Класс Status

Описание класса Модель статусов документов.

## Методы

| Signature        | Decorator | Docstring                                                                                                             |
| :--------------- | :-------- | :-------------------------------------------------------------------------------------------------------------------- |
| name(unknown)    | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| edit(unknown)    | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| comment(unknown) | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| id(unknown)      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| objects(unknown) | -         |                                                                                                                       |

# Класс Sheet

Описание класса Модель листа для вывода.

## Методы

| Signature                           | Decorator | Docstring                                                                                                                                                                     |
| :---------------------------------- | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name(unknown)                       | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| position(unknown)                   | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| comment(unknown)                    | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| created_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| updated_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_next_by_created_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| id(unknown)                         | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| objects(unknown)                    | -         |                                                                                                                                                                               |

# Класс Document

Описание класса Модель документа. Когда начинается сбор, берутся атрибуты и листы привязанные к периоду. На основе листов и атрибутов создается документ для дивизиона. sheet - список листов в собираемом документе. content_type - Department, Organization - выбирается из проекта. object_id - идентификатор Department, Organization. None в случае если для всех дивизионов один сбор.

## Методы

| Signature                           | Decorator | Docstring                                                                                                                                                                     |
| :---------------------------------- | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| comment(unknown)                    | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| version(unknown)                    | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| created_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| updated_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| object_id(unknown)                  | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_next_by_created_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| id(unknown)                         | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| objects(unknown)                    | -         |                                                                                                                                                                               |

# Класс DocumentStatus

Описание класса Модель статуса документа.

## Методы

| Signature                           | Decorator | Docstring                                                                                                                                                                     |
| :---------------------------------- | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| comment(unknown)                    | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| created_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_next_by_created_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| id(unknown)                         | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| objects(unknown)                    | -         |                                                                                                                                                                               |

# Класс Attribute

Описание класса Не табличные данные хранятся в атрибутах. Модель содержит список не табличных данных для организации сбора в указанный период. Информация о типах: - TEXT - тестовое поле - MONEY - поле для ввода денег

## Методы

| Signature                 | Decorator | Docstring                                                                                                                                                                     |
| :------------------------ | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name(unknown)             | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| placeholder(unknown)      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| key(unknown)              | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| kind(unknown)             | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| default(unknown)          | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| mutable(unknown)          | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_kind_display(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| id(unknown)               | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| objects(unknown)          | -         |                                                                                                                                                                               |

# Класс AttributeValue

Описание класса Модель значения параметра.

## Методы

| Signature                           | Decorator | Docstring                                                                                                                                                                     |
| :---------------------------------- | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| value(unknown)                      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| created_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| updated_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_next_by_created_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| id(unknown)                         | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| objects(unknown)                    | -         |                                                                                                                                                                               |