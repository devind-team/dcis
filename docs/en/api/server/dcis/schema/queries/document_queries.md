# Модуль document_queries



## Класс DocumentQueries

Запросы записей, связанных с документами.

### Методы

| Сигнатура                                                                                                                                            | Декораторы       | Описание |
| :--------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------- | :------- |
| resolve_documents( root: Any, info: graphql.execution.base.ResolveInfo, period_id: str, divisions_id: list[str] = [])                                | ['staticmethod'] | -        |
| resolve_document( root, info: graphql.execution.base.ResolveInfo, document_id: str, *args, **kwargs) -&#62; apps.dcis.models.document.Document       | ['staticmethod'] | -        |
| resolve_document_statuses( root, info: graphql.execution.base.ResolveInfo, document_id: str, *args, **kwargs) -&#62; django.db.models.query.QuerySet | ['staticmethod'] | -        |