# Модуль document_queries



## Класс DocumentQueries

Запросы записей, связанных с документами.

### Методы

| Сигнатура                                                                                                                           | Декораторы                                                        | Описание |
| :---------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------- | :------- |
| resolve_documents( root: Any, info: graphql.execution.base.ResolveInfo, period_id: str) -&#62; django.db.models.query.QuerySet      | staticmethod, permission_classes((IsAuthenticated,))              | -        |
| resolve_document( root, info: graphql.execution.base.ResolveInfo, document_id: str) -&#62; apps.dcis.models.document.Document       | staticmethod, permission_classes((IsAuthenticated, ViewDocument)) | -        |
| resolve_statuses( root, info: graphql.execution.base.ResolveInfo) -&#62; django.db.models.query.QuerySet                            | staticmethod, permission_classes((IsAuthenticated,))              | -        |
| resolve_document_statuses( root, info: graphql.execution.base.ResolveInfo, document_id: str) -&#62; django.db.models.query.QuerySet | staticmethod, permission_classes((IsAuthenticated, ViewDocument)) | -        |