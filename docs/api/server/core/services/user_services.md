# Модуль user_services



### Функции

| Сигнатура                                                                                                                                       | Декораторы | Описание                                         |
| :---------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :----------------------------------------------- |
| relation_division( user: apps.core.models.User, data: dict[str, typing.Union[str, int]]) -&#62; None                                            | -          | Привязка авторизуемого пользователя к дивизиону. |
| get_user_from_id_or_context( info: graphql.execution.base.ResolveInfo, user_id: str &#124; int &#124; None = None) -&#62; apps.core.models.User | -          | Получаем пользователя                            |