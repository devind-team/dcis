# Модуль period_queries



## Класс PeriodQueries

Запросы записей, связанных с периодами.

### Методы

| Сигнатура                                                                                                                                                        | Декораторы                                                      | Описание |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------- | :------- |
| resolve_privileges( root, info: graphql.execution.base.ResolveInfo) -&#62; django.db.models.query.QuerySet                                                       | staticmethod, permission_classes((IsAuthenticated,))            | -        |
| resolve_period( root: Any, info: graphql.execution.base.ResolveInfo, period_id: str) -&#62; apps.dcis.models.project.Period                                      | staticmethod, permission_classes((IsAuthenticated, ViewPeriod)) | -        |
| resolve_periods( root: Any, info: graphql.execution.base.ResolveInfo, project_id: str) -&#62; django.db.models.query.QuerySet                                    | staticmethod, permission_classes((IsAuthenticated,))            | -        |
| resolve_period_users( root: Any, info: graphql.execution.base.ResolveInfo, period_id: str) -&#62; django.db.models.query.QuerySet                                | staticmethod, permission_classes((IsAuthenticated, ViewPeriod)) | -        |
| resolve_user_period_privileges( root, info: graphql.execution.base.ResolveInfo, user_id: str &#124; None, period_id: str) -&#62; django.db.models.query.QuerySet | staticmethod, permission_classes((IsAuthenticated, ViewPeriod)) | -        |
| resolve_sheet( root: Any, info: graphql.execution.base.ResolveInfo, sheet_id: str, document_id: str &#124; None = None)                                          | staticmethod, permission_classes((IsAuthenticated,))            | -        |
| resolve_value_files( root, info: graphql.execution.base.ResolveInfo, document_id: str, sheet_id: str, column_id: str, row_id: str)                               | staticmethod, permission_classes((IsAuthenticated,))            | -        |