# Модуль section_permissions



## Класс AddSection

Пропускает пользователей, которые могут добавлять секции на страницу

### Методы

| Сигнатура                                                        | Декораторы   | Описание                                                                                                                                |
| :--------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                       | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.pages.models.page.Page) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangeSection

Пропускает пользователей, которые могут изменять секцию

### Методы

| Сигнатура                                                                  | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                                 | -            | -                                                                                                                                       |
| has_object_permission(context, section: apps.pages.models.section.Section) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс DeleteSection

Пропускает пользователей, которые могут удалять секцию

### Методы

| Сигнатура                                                                  | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                                 | -            | -                                                                                                                                       |
| has_object_permission(context, section: apps.pages.models.section.Section) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |