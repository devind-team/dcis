# Модуль sheet_queries



## Класс SheetQueries

Запросы записей, связанных с листами для вывода.

### Методы

| Signature                                                                                                                          | Decorator                                                    | Docstring |
| :--------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| resolve_sheet( root: Any, info: graphql.execution.base.ResolveInfo, sheet_id: str, document_id: Optional[str] = None)              | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |
| resolve_value_files( root, info: graphql.execution.base.ResolveInfo, document_id: str, sheet_id: str, column_id: str, row_id: str) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |