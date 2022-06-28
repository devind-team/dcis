# Модуль project_mutations

Описание модуля

# Класс AddProjectMutationPayload

Описание класса Мутация для добавления проекта.

## Методы

| Signature                                                                                                    | Decorator        | Docstring |
| :----------------------------------------------------------------------------------------------------------- | :--------------- | :-------- |
| validate( cls, root: Any, info: graphql.execution.base.ResolveInfo, input, *args, **kwargs)                  | ['@classmethod'] |           |
| handle_content_type( cls, value: str, field: str, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['@classmethod'] |           |

# Класс ChangeProjectMutationPayload

Описание класса Мутация изменения настроек проекта.

# Класс DeleteProjectMutationPayload

Описание класса Мутация на удаление проекта.

# Класс AddPeriodMutation

Описание класса Мутация для создания периода.

## Методы

| Signature                                                                                                                                                                           | Decorator                                                              | Docstring |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, name: str, project_id: str, file: django.core.files.uploadedfile.InMemoryUploadedFile, multiple: bool) | ['@staticmethod', '@permission_classes((IsAuthenticated, AddPeriod))'] |           |

# Класс ChangePeriodMutationPayload

Описание класса Мутация на изменение настроек периода.

# Класс DeletePeriodMutationPayload

Описание класса Мутация на удаление периода.

# Класс ChangeDivisionsMutation

Описание класса Мутация на изменение дивизионов.

## Методы

| Signature                                                                                                             | Decorator                                                    | Docstring |
| :-------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, period_id: str, division_ids: list[str]) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

# Класс DeleteDivisionsMutationPayload

Описание класса Мутация на удаление объекта из периода.

# Класс AddPeriodGroupMutationPayload

Описание класса Мутация на добавление группы периода.

# Класс CopyPeriodGroupMutation

Описание класса Мутация на перенос группы с пользователями из другого сбора.

## Методы

| Signature                                                                                                                                           | Decorator                                                    | Docstring |
| :-------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, period_id: str, selected_period_id: str, period_groups_ids: list[str]) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

# Класс ChangePeriodGroupUsersMutation

Описание класса Мутация на добавление пользователей в группу.

## Методы

| Signature                                                                                                                | Decorator                                                    | Docstring |
| :----------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, period_group_id: str, users_ids: list[str]) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

# Класс DeletePeriodGroupMutationPayload

Описание класса Мутация на удаление группы сбора.

# Класс DeleteUserFromPeriodGroupMutation

Описание класса Мутация на удаление пользователя из группы.

## Методы

| Signature                                                                                                        | Decorator                                                    | Docstring |
| :--------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, period_group_id: str, user_id: str) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

# Класс ProjectMutations

Описание класса Список мутация проекта.