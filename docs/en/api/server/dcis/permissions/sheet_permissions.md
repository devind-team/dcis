# Модуль sheet_permissions



## Класс ChangeSheet

Пропускает пользователей, которые могут менять структуру листа.

### Методы

| Сигнатура                                                            | Декораторы       | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -                | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.document.Sheet) | ['staticmethod'] | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс AddChildRowDimension

Пропускает пользователей, которые могут добавлять дочерние строки к строке.

### Методы

| Сигнатура                                                                | Декораторы       | Описание                                                                                                                                |
| :----------------------------------------------------------------------- | :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                               | -                | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.sheet.RowDimension) | ['staticmethod'] | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс DeleteRowDimension

Пропускает пользователей, которые могут удалять строку.

### Методы

| Сигнатура                                                                | Декораторы       | Описание                                                                                                                                |
| :----------------------------------------------------------------------- | :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                               | -                | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.sheet.RowDimension) | ['staticmethod'] | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ViewDocument

Пропускает пользователей, которые могут просматривать документ.

### Методы

| Сигнатура                                                               | Декораторы       | Описание                                                                                                                                |
| :---------------------------------------------------------------------- | :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                              | -                | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.document.Document) | ['staticmethod'] | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |