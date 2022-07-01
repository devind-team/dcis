# Модуль sheet



### Функции

| Сигнатура            | Декораторы | Описание                          |
| :------------------- | :--------- | :-------------------------------- |
| get_default_border() | -          | Стиль и цвет границ по умолчанию. |

## Класс Style

Абстрактная модель применяемых стилей для страниц сборов.

### Методы

| Сигнатура                             | Декораторы | Описание                                                                                                                                                                      |
| :------------------------------------ | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_horizontal_align_display(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_vertical_align_display(unknown)   | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_underline_display(unknown)        | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс KindCell

Классификация ячеек.

### Методы

| Сигнатура                 | Декораторы | Описание                                                                                                                                                                      |
| :------------------------ | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_kind_display(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс ColumnDimension

Модель стилей для колонки таблицы. Ссылка на оригинальный класс из openpyxl: https://foss.heptapod.net/openpyxl/openpyxl/-/blob/branch/3.0/openpyxl/worksheet/dimensions.py

### Методы

| Сигнатура                           | Декораторы | Описание                                                                                                                                                                      |
| :---------------------------------- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_next_by_created_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_kind_display(unknown)           | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс RowDimension

Модель стилей для строки таблицы. Кроме того, что таблица плоская, могут быть еще промежуточные агрегаций, они реализуются с помощью дополнительных полей. - dynamic - описывает динамическую строку - aggregation - способ агрегации дочерних строк (SUM, MIN, MAX, AVG) - parent - ссылка на родительскую строку - document - ссылка на документ. Это поле необходимо для того, чтобы к обычным строкам плоской таблицы добавлять динамические строки, которые не относятся к определенному документу, однако, должны участвовать при заполнении финальной версии документа.

### Методы

| Сигнатура                           | Декораторы | Описание                                                                                                                                                                      |
| :---------------------------------- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_aggregation_display(unknown)    | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_created_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_created_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_next_by_updated_at(unknown)     | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_previous_by_updated_at(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс Cell

Модель ячейки.

### Методы

| Сигнатура                             | Декораторы | Описание                                                                                                                                                                      |
| :------------------------------------ | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_horizontal_align_display(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_vertical_align_display(unknown)   | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_underline_display(unknown)        | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_kind_display(unknown)             | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс Limitation

Накладываемые на ячейку ограничения.

### Методы

| Сигнатура                      | Декораторы | Описание                                                                                                                                                                      |
| :----------------------------- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_operator_display(unknown)  | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |
| get_condition_display(unknown) | -          | Method descriptor with partial application of the given argumentsand keywords.Supports wrapping existing descriptors and handles non-descriptorcallables as instance methods. |

## Класс MergedCell

Модель объединенной ячейки.

### Методы

| Сигнатура            | Декораторы | Описание          |
| :------------------- | :--------- | :---------------- |
| __str__(self) -> str | -          | Return str(self). |

## Класс Value

Модель значения поля таблицы. Привязка значения осуществляется к дивизиону через документ, но в документе может быть несколько листов. В связи с этим добавлено поле sheet, которое точно определяет к какому листу имеет отношение таблицы.