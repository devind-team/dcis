# Модуль privilege_queries



## Класс PrivilegeQueries

Запросы записей, связанных с привилегиями.

### Методы

| Сигнатура                                                                                                                                                                    | Декораторы                                                 | Описание |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------- | :------- |
| resolve_user_group_privileges( root, info: graphql.execution.base.ResolveInfo, period_group_id: int, user_id: str &#124; None = None) -&#62; django.db.models.query.QuerySet | ['staticmethod', 'permission_classes((IsAuthenticated,))'] | -        |
| resolve_user_period_privileges( root, info: graphql.execution.base.ResolveInfo, period_id: str, user_id: str &#124; None = None) -&#62; django.db.models.query.QuerySet      | ['staticmethod', 'permission_classes((IsAuthenticated,))'] | -        |
| resolve_additional_privileges( root, info: graphql.execution.base.ResolveInfo, period_id: str, user_id: str, *args, **kwargs) -&#62; django.db.models.query.QuerySet         | ['staticmethod', 'permission_classes((IsAuthenticated,))'] | -        |