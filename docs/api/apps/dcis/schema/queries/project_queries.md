# Модуль project_queries



## Класс ProjectQueries

Запросы записей, связанных с проектами.

### Методы

| Signature                                                                                                                                             | Decorator                                                    | Docstring |
| :---------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| resolve_project( root: Any, info: graphql.execution.base.ResolveInfo, project_id: str, *args, **kwargs)                                               | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |
| resolve_projects(root: Any, info: graphql.execution.base.ResolveInfo, *args, **kwargs)                                                                | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |
| resolve_period( root: Any, info: graphql.execution.base.ResolveInfo, period_id: str, *args, **kwargs)                                                 | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |
| resolve_periods( root: Any, info: graphql.execution.base.ResolveInfo, project_id: str, *args, **kwargs)                                               | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |
| resolve_user_divisions( root: Any, info: graphql.execution.base.ResolveInfo, user_id: Optional[str] = None, project_id: Optional[str] = None) -> list | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |
| resolve_divisions( root: Any, info: graphql.execution.base.ResolveInfo, period_id: int, *args, **kwargs)                                              | ['@staticmethod']                                            |           |