# Модуль privilege_mutations

Описание модуля

# Класс ChangePeriodGroupPrivilegesMutation

Описание класса Мутация на изменение привилегий группы.

## Методы

| Signature                                                                                                                     | Decorator                                                    | Docstring |
| :---------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, period_group_id: int, privileges_ids: list[str]) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

# Класс ChangeGroupUserPrivilegesMutation

Описание класса Мутация на изменение привилегий пользователя.

## Методы

| Signature                                                                                                                                   | Decorator                                                    | Docstring |
| :------------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, period_group_id: str, user_id: str, privileges_ids: list[str]) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

# Класс PrivilegeMutations

Описание класса Список мутация привилегий.