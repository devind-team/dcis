# Модуль user_services

Описание модуля

# Функции

| Signature                                                                                                                         | Decorator | Docstring                                        |
| :-------------------------------------------------------------------------------------------------------------------------------- | :-------- | :----------------------------------------------- |
| relation_division( user: apps.core.models.User, data: dict[str, typing.Union[str, int]]) -> None                                  | -         | Привязка авторизуемого пользователя к дивизиону. |
| get_user_from_id_or_context( info: graphql.execution.base.ResolveInfo, user_id: str | int | None = None) -> apps.core.models.User | -         | Получаем пользователя                            |