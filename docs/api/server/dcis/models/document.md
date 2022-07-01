# Модуль document



## Класс Status

Модель статусов документов.

## Класс Sheet

Модель листа для вывода.

### Методы

| Сигнатура                           | Декораторы | Описание                                                                                                                                                                      |
| :---------------------------------- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_next_by_created_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс Document

Модель документа. Когда начинается сбор, берутся атрибуты и листы привязанные к периоду. На основе листов и атрибутов создается документ для дивизиона. sheet - список листов в собираемом документе. content_type - Department, Organization - выбирается из проекта. object_id - идентификатор Department, Organization. None в случае если для всех дивизионов один сбор.

### Методы

| Сигнатура                           | Декораторы | Описание                                                                                                                                                                      |
| :---------------------------------- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_next_by_created_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс DocumentStatus

Модель статуса документа.

### Методы

| Сигнатура                           | Декораторы | Описание                                                                                                                                                                      |
| :---------------------------------- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_next_by_created_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс Attribute

Не табличные данные хранятся в атрибутах. Модель содержит список не табличных данных для организации сбора в указанный период. Информация о типах: - TEXT - тестовое поле - MONEY - поле для ввода денег

### Методы

| Сигнатура                 | Декораторы | Описание                                                                                                                                                                      |
| :------------------------ | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_kind_display(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс AttributeValue

Модель значения параметра.

### Методы

| Сигнатура                           | Декораторы | Описание                                                                                                                                                                      |
| :---------------------------------- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_next_by_created_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |