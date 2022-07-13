# Модуль project_queries



## Класс ProjectQueries

Запросы записей, связанных с проектами.

### Методы

| Сигнатура                                                                                                                               | Декораторы                                                       | Описание |
| :-------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------- | :------- |
| resolve_project( root: Any, info: graphql.execution.base.ResolveInfo, project_id: str) -&#62; apps.dcis.models.project.Project          | staticmethod, permission_classes((IsAuthenticated, ViewProject)) | -        |
| resolve_projects( root: Any, info: graphql.execution.base.ResolveInfo, *args, **kwargs) -&#62; django.db.models.query.QuerySet          | staticmethod, permission_classes((IsAuthenticated,))             | -        |
| resolve_project_divisions( root: Any, info: graphql.execution.base.ResolveInfo, project_id: str) -&#62; list[dict[str, int &#124; str]] | staticmethod, permission_classes((IsAuthenticated, ViewProject)) | -        |