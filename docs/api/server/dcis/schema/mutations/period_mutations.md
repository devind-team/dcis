# Модуль period_mutations



## Класс AddPeriodMutation

Мутация для создания периода.

### Методы

| Сигнатура                                                                                                                                                                           | Декораторы                                                     | Описание |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, name: str, project_id: str, file: django.core.files.uploadedfile.InMemoryUploadedFile, multiple: bool) | staticmethod, permission_classes((IsAuthenticated, AddPeriod)) | -        |

## Класс ChangePeriodMutationPayload

Мутация на изменение настроек периода.

### Методы

| Сигнатура                                                                                                                                           | Декораторы  | Описание |
| :-------------------------------------------------------------------------------------------------------------------------------------------------- | :---------- | :------- |
| check_permissions( cls, root: Any, info: graphql.execution.base.ResolveInfo, input: Any, id: str, obj: apps.dcis.models.project.Period) -&#62; None | classmethod | -        |

## Класс DeletePeriodMutationPayload

Мутация на удаление периода.

### Методы

| Сигнатура                                                                                                                               | Декораторы  | Описание |
| :-------------------------------------------------------------------------------------------------------------------------------------- | :---------- | :------- |
| check_permissions( cls, root: Any, info: graphql.execution.base.ResolveInfo, id: str, obj: apps.dcis.models.project.Period) -&#62; None | classmethod | -        |

## Класс AddDivisionsMutation

Мутация на добавление дивизионов в период.

### Методы

| Сигнатура                                                                                                             | Декораторы                                                                 | Описание |
| :-------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, period_id: str, division_ids: list[str]) | staticmethod, permission_classes((IsAuthenticated, ChangePeriodDivisions)) | -        |

## Класс DeleteDivisionMutation

Мутация на удаление дивизиона из периода.

### Методы

| Сигнатура                                                                                                      | Декораторы                                                                 | Описание |
| :------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, period_id: str, division_id: str) | staticmethod, permission_classes((IsAuthenticated, ChangePeriodDivisions)) | -        |

## Класс AddPeriodGroupMutationPayload

Мутация на добавление группы периода.

### Методы

| Сигнатура                                                                                            | Декораторы  | Описание |
| :--------------------------------------------------------------------------------------------------- | :---------- | :------- |
| check_permissions( cls, root: Any, info: graphql.execution.base.ResolveInfo, input: Any) -&#62; None | classmethod | -        |

## Класс CopyPeriodGroupsMutation

Мутация на перенос групп с пользователями из другого периода.

### Методы

| Сигнатура                                                                                                                                          | Декораторы                                                              | Описание |
| :------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, period_id: str, selected_period_id: str, period_group_ids: list[str]) | staticmethod, permission_classes((IsAuthenticated, ChangePeriodGroups)) | -        |

## Класс ChangePeriodGroupPrivilegesMutation

Мутация на изменение привилегий группы.

### Методы

| Сигнатура                                                                                                                     | Декораторы                                                              | Описание |
| :---------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, period_group_id: int, privileges_ids: list[str]) | staticmethod, permission_classes((IsAuthenticated, ChangePeriodGroups)) | -        |

## Класс DeletePeriodGroupMutationPayload

Мутация на удаление группы периода.

### Методы

| Сигнатура                                                                                                                                      | Декораторы  | Описание |
| :--------------------------------------------------------------------------------------------------------------------------------------------- | :---------- | :------- |
| check_permissions( cls, root: Any, info: graphql.execution.base.ResolveInfo, id: str, obj: apps.dcis.models.privilege.PeriodGroup) -&#62; None | classmethod | -        |

## Класс ChangeUserPeriodGroupsMutation

Мутация на изменение групп пользователя в периоде.

### Методы

| Сигнатура                                                                                                                                                  | Декораторы                                                             | Описание |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, user_id: str, period_group_ids: list[apps.dcis.models.privilege.PeriodGroup]) | staticmethod, permission_classes((IsAuthenticated, ChangePeriodUsers)) | -        |

## Класс ChangeUserPeriodPrivileges

Мутация на изменение отдельных привилегий пользователя в периоде.

### Методы

| Сигнатура                                                                                                                             | Декораторы                                                             | Описание |
| :------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, user_id: str, period_id: str, privileges_ids: list[str]) | staticmethod, permission_classes((IsAuthenticated, ChangePeriodUsers)) | -        |

## Класс PeriodMutations

Список мутация периода.