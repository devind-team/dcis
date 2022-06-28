# Модуль project

Описание модуля

# Функции

| Signature                      | Decorator | Docstring |
| :----------------------------- | :-------- | :-------- |
| default_content_type(instance) | -         |           |

# Класс Project

Описание класса Проект сборов.

## Методы

| Signature                           | Decorator | Docstring                                                                                                                                                                     |
| :---------------------------------- | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name(unknown)                       | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| short(unknown)                      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| description(unknown)                | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| visibility(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| archive(unknown)                    | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| created_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| updated_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_next_by_created_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| id(unknown)                         | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| objects(unknown)                    | -         |                                                                                                                                                                               |

# Класс Period

Описание класса Модель периода проекта. - multiple - множественное заполнение, в случае если False, предоставляется один документ на все дивизионы. - privately - приватность отвечает за видимость добавленных строк, предоставляется ли доступ ко всем строкам или только к тем, которые добавил я. Это определяет условие выгрузки строк: - все строки - у меня есть права или privately = False - только строки пользователя - нет прав и privately = True

## Методы

| Signature                           | Decorator | Docstring                                                                                                                                                                     |
| :---------------------------------- | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name(unknown)                       | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| status(unknown)                     | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| multiple(unknown)                   | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| privately(unknown)                  | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| start(unknown)                      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| expiration(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| created_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| updated_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_status_display(unknown)         | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_created_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| id(unknown)                         | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| objects(unknown)                    | -         |                                                                                                                                                                               |

# Класс Division

Описание класса Участвующие в сборах подразделения. Реализация будет осуществляться для двух дивизионов: - Department - департамент - Organization - организации Связь к дивизионам или департамента обеспечивается через content_object

## Методы

| Signature          | Decorator | Docstring                                                                                                             |
| :----------------- | :-------- | :-------------------------------------------------------------------------------------------------------------------- |
| object_id(unknown) | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| id(unknown)        | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| objects(unknown)   | -         |                                                                                                                       |