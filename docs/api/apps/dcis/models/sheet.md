# Модуль sheet



### Функции

| Signature            | Decorator | Docstring                         |
| :------------------- | :-------- | :-------------------------------- |
| get_default_border() | -         | Стиль и цвет границ по умолчанию. |

## Класс Style

Абстрактная модель применяемых стилей для страниц сборов.

### Методы

| Signature                             | Decorator | Docstring                                                                                                                                                                     |
| :------------------------------------ | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| horizontal_align(unknown)             | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| vertical_align(unknown)               | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| size(unknown)                         | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| strong(unknown)                       | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| italic(unknown)                       | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| strike(unknown)                       | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| underline(unknown)                    | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| color(unknown)                        | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| background(unknown)                   | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| border_style(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| border_color(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_horizontal_align_display(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_vertical_align_display(unknown)   | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_underline_display(unknown)        | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс KindCell

Классификация ячеек.

### Методы

| Signature                 | Decorator | Docstring                                                                                                                                                                     |
| :------------------------ | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| kind(unknown)             | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_kind_display(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс ColumnDimension

Модель стилей для колонки таблицы. Ссылка на оригинальный класс из openpyxl: https://foss.heptapod.net/openpyxl/openpyxl/-/blob/branch/3.0/openpyxl/worksheet/dimensions.py

### Методы

| Signature                           | Decorator | Docstring                                                                                                                                                                     |
| :---------------------------------- | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| index(unknown)                      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| width(unknown)                      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| fixed(unknown)                      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| hidden(unknown)                     | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| created_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| updated_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_next_by_created_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_kind_display(unknown)           | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| id(unknown)                         | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| objects(unknown)                    | -         |                                                                                                                                                                               |

## Класс RowDimension

Модель стилей для строки таблицы. Кроме того, что таблица плоская, могут быть еще промежуточные агрегаций, они реализуются с помощью дополнительных полей. - dynamic - описывает динамическую строку - aggregation - способ агрегации дочерних строк (SUM, MIN, MAX, AVG) - parent - ссылка на родительскую строку - document - ссылка на документ. Это поле необходимо для того, чтобы к обычным строкам плоской таблицы добавлять динамические строки, которые не относятся к определенному документу, однако, должны участвовать при заполнении финальной версии документа.

### Методы

| Signature                           | Decorator | Docstring                                                                                                                                                                     |
| :---------------------------------- | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| index(unknown)                      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| height(unknown)                     | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| fixed(unknown)                      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| hidden(unknown)                     | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| dynamic(unknown)                    | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| object_id(unknown)                  | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| aggregation(unknown)                | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| created_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| updated_at(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_aggregation_display(unknown)    | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_created_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| id(unknown)                         | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| objects(unknown)                    | -         |                                                                                                                                                                               |

## Класс Cell

Модель ячейки.

### Методы

| Signature                             | Decorator | Docstring                                                                                                                                                                     |
| :------------------------------------ | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| editable(unknown)                     | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| formula(unknown)                      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| comment(unknown)                      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| default(unknown)                      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| mask(unknown)                         | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| tooltip(unknown)                      | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_horizontal_align_display(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_vertical_align_display(unknown)   | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_underline_display(unknown)        | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_kind_display(unknown)             | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| id(unknown)                           | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| objects(unknown)                      | -         |                                                                                                                                                                               |

## Класс Limitation

Накладываемые на ячейку ограничения.

### Методы

| Signature                      | Decorator | Docstring                                                                                                                                                                     |
| :----------------------------- | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| operator(unknown)              | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| condition(unknown)             | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| value(unknown)                 | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| get_operator_display(unknown)  | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_condition_display(unknown) | -         | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| id(unknown)                    | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed.                                                         |
| objects(unknown)               | -         |                                                                                                                                                                               |

## Класс MergedCell

Модель объединенной ячейки.

### Методы

| Signature            | Decorator | Docstring                                                                                                             |
| :------------------- | :-------- | :-------------------------------------------------------------------------------------------------------------------- |
| min_col(unknown)     | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| min_row(unknown)     | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| max_col(unknown)     | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| max_row(unknown)     | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| __str__(self) -> str | -         | Return str(self).                                                                                                     |
| id(unknown)          | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| objects(unknown)     | -         |                                                                                                                       |

## Класс Value

Модель значения поля таблицы. Привязка значения осуществляется к дивизиону через документ, но в документе может быть несколько листов. В связи с этим добавлено поле sheet, которое точно определяет к какому листу имеет отношение таблицы.

### Методы

| Signature         | Decorator | Docstring                                                                                                             |
| :---------------- | :-------- | :-------------------------------------------------------------------------------------------------------------------- |
| value(unknown)    | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| payload(unknown)  | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| verified(unknown) | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| error(unknown)    | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| id(unknown)       | -         | A wrapper for a deferred-loading field. When the value is read from thisobject the first time, the query is executed. |
| objects(unknown)  | -         |                                                                                                                       |