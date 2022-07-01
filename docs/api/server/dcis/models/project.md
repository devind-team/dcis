# Модуль project



### Функции

| Сигнатура                      | Декораторы | Описание |
| :----------------------------- | :--------- | :------- |
| default_content_type(instance) | -          | -        |

## Класс Project

Проект сборов.

### Методы

| Сигнатура                           | Декораторы | Описание                                                                                                                                                                      |
| :---------------------------------- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_next_by_created_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс Period

Модель периода проекта. - multiple - множественное заполнение, в случае если False, предоставляется один документ на все дивизионы. - privately - приватность отвечает за видимость добавленных строк, предоставляется ли доступ ко всем строкам или только к тем, которые добавил я. Это определяет условие выгрузки строк: - все строки - у меня есть права или privately = False - только строки пользователя - нет прав и privately = True

### Методы

| Сигнатура                           | Декораторы | Описание                                                                                                                                                                      |
| :---------------------------------- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_status_display(unknown)         | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_created_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс Division

Участвующие в сборах подразделения. Реализация будет осуществляться для двух дивизионов: - Department - департамент - Organization - организации Связь к дивизионам или департамента обеспечивается через content_object