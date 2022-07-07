# Модуль privilege_mutations



## Класс ChangePeriodGroupPrivilegesMutation

Мутация на изменение привилегий группы.

### Методы

| Сигнатура                                                                                                                     | Декораторы                                                 | Описание |
| :---------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, period_group_id: int, privileges_ids: list[str]) | ['staticmethod', 'permission_classes((IsAuthenticated,))'] | -        |

## Класс ChangeGroupUserPrivilegesMutation

Мутация на изменение привилегий пользователя.

### Методы

| Сигнатура                                                                                                                                   | Декораторы                                                 | Описание |
| :------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, period_group_id: str, user_id: str, privileges_ids: list[str]) | ['staticmethod', 'permission_classes((IsAuthenticated,))'] | -        |

## Класс PrivilegeMutations

Список мутация привилегий.