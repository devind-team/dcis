# Модуль mutations



## Класс AuthCbiasMutation

Мутация для авторизации пользователя через портал https://cbias.ru.

### Методы

| Signature                                                                                                     | Decorator         | Docstring                         |
| :------------------------------------------------------------------------------------------------------------ | :---------------- | :-------------------------------- |
| get_user( info: graphql.execution.base.ResolveInfo, payload: dict, data: dict) -> apps.core.models.User       | ['@staticmethod'] | Получение пользователя по данным. |
| callback( info: graphql.execution.base.ResolveInfo, access_token: oauth2_provider.models.AccessToken) -> None | ['@staticmethod'] |                                   |