# Модуль document_queries



## Класс DocumentQueries

Запросы записей, связанных с документами.

### Методы

| Signature                                                                                                                                        | Decorator         | Docstring |
| :----------------------------------------------------------------------------------------------------------------------------------------------- | :---------------- | :-------- |
| resolve_documents( root: Any, info: graphql.execution.base.ResolveInfo, period_id: str, divisions_id: list[str] = [])                            | ['@staticmethod'] | -         |
| resolve_document( root, info: graphql.execution.base.ResolveInfo, document_id: str, *args, **kwargs) -> apps.dcis.models.document.Document       | ['@staticmethod'] | -         |
| resolve_document_statuses( root, info: graphql.execution.base.ResolveInfo, document_id: str, *args, **kwargs) -> django.db.models.query.QuerySet | ['@staticmethod'] | -         |