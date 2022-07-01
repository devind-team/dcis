# Модуль types



## Класс UserType

Описание пользовательского типа.

### Методы

| Сигнатура                                                                                                                         | Декораторы                                                           | Описание |
| :-------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------- | :------- |
| resolve_session( user: apps.core.models.User, info: graphql.execution.base.ResolveInfo) -> django.db.models.query.QuerySet        | ['@staticmethod']                                                    | -        |
| resolve_groups( user: apps.core.models.User, info: graphql.execution.base.ResolveInfo) -> django.db.models.query.QuerySet         | ['@staticmethod', "@resolver_hints(model_field='groups')"]           | -        |
| resolve_permissions( user: apps.core.models.User, info: graphql.execution.base.ResolveInfo) -> Set[str]                           | ['@staticmethod', "@resolver_hints(model_field='user_permissions')"] | -        |
| resolve_notices( user: apps.core.models.User, info: graphql.execution.base.ResolveInfo) -> django.db.models.query.QuerySet        | ['@staticmethod', "@resolver_hints(model_field='notice_set')"]       | -        |
| resolve_notifications( user: apps.core.models.User, info: graphql.execution.base.ResolveInfo) -> django.db.models.query.QuerySet  | ['@staticmethod', "@resolver_hints(model_field='notification_set')"] | -        |
| resolve_profile_values( user: apps.core.models.User, info: graphql.execution.base.ResolveInfo) -> django.db.models.query.QuerySet | ['@staticmethod', "@resolver_hints(model_field='profilevalue_set')"] | -        |
| resolve_divisions( user: apps.core.models.User, info: graphql.execution.base.ResolveInfo)                                         | ['@staticmethod']                                                    | -        |