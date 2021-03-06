# Модуль period_permissions

Разрешения на работу с периодами проектов.

## Класс ViewPeriod

Пропускает пользователей, которые могут просматривать период.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс AddPeriodBase

Пропускает пользователей, которые могут добавлять периоды в проект, без проверки возможности просмотра.

### Методы

| Сигнатура                                                             | Декораторы   | Описание                                                                                                                                |
| :-------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                            | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Project) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс AddPeriod

Пропускает пользователей, которые могут просматривать проект и добавлять в него периоды.

### Методы

| Сигнатура                                                             | Декораторы   | Описание                                                                                                                                |
| :-------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                            | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Project) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangePeriodBase

Пропускает пользователей, которые могут изменять период в проекте, без проверки возможности просмотра.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangePeriod

Пропускает пользователей, которые могут просматривать и изменять период в проекте.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangePeriodDivisionsBase

Пропускает пользователей, которые могут изменять дивизионы периода, без проверки возможности просмотра.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangePeriodDivisions

Пропускает пользователей, которые могут просматривать период и изменять в нем дивизионы.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangePeriodGroupsBase

Пропускает пользователей, которые могут изменять группы периода, без проверки возможности просмотра.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangePeriodGroups

Пропускает пользователей, которые могут просматривать период и изменять в нем группы.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangePeriodUsersBase

Пропускает пользователей, которые могут изменять пользователей периода, без проверки возможности просмотра.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangePeriodUsers

Пропускает пользователей, которые могут просматривать период и изменять в нем пользователей.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangePeriodSettingsBase

Пропускает пользователей, которые могут изменять настройки периода, без проверки возможности просмотра.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangePeriodSettings

Пропускает пользователей, которые могут просматривать период и изменять в нем настройки.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangePeriodSheetBase

Пропускает пользователей, которые могут изменять структуру листа, без проверки возможности просмотра.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс ChangePeriodSheet

Пропускает пользователей, которые могут просматривать период и изменять в нем структуру листа.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс DeletePeriodBase

Пропускает пользователей, которые могут удалять период, без проверки возможности просмотра.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |

## Класс DeletePeriod

Пропускает пользователей, которые могут просматривать и удалять период в проекте.

### Методы

| Сигнатура                                                            | Декораторы   | Описание                                                                                                                                |
| :------------------------------------------------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| __init__()                                                           | -            | -                                                                                                                                       |
| has_object_permission(context, obj: apps.dcis.models.project.Period) | staticmethod | Возвращает True если есть права, False в противном случае.:param context: контекст:param obj: объект для проверки:return: есть ли права |