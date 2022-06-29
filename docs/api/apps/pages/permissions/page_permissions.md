# Модуль page_permissions



## Класс ChangePage

Пропускает пользователей, которые могут изменять страницу

### Методы

| Signature                                                        | Decorator         | Docstring                                                                                                                               |
| :--------------------------------------------------------------- | :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                       | -                 | -                                                                                                                                       |
| has_object_permission(context, obj: apps.pages.models.page.Page) | ['@staticmethod'] | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс DeletePage

Пропускает пользователей, которые могут удалять страницу

### Методы

| Signature                                                        | Decorator         | Docstring                                                                                                                               |
| :--------------------------------------------------------------- | :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                       | -                 | -                                                                                                                                       |
| has_object_permission(context, obj: apps.pages.models.page.Page) | ['@staticmethod'] | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |