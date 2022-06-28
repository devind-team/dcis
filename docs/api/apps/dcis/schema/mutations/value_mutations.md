# Модуль value_mutations

Модуль содержит мутации, относящиеся к значениям ячеек.

## Класс ChangeValueMutation

Изменение значения ячейки.

### Методы

| Signature                                                                                                                                              | Decorator                                                                | Docstring |
| :----------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, document_id: str, sheet_id: str, column_id: str, row_id: str, value: str) | ['@staticmethod', '@permission_classes((IsAuthenticated, ChangeValue))'] |           |

## Класс ChangeFileValueMutation

Изменение значения ячейки типа `Файл`.

### Методы

| Signature                                                                                                                                                                                                                                                | Decorator                                                                | Docstring |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, document_id: str, sheet_id: str, column_id: str, row_id: str, value: str, remaining_files: list[str], new_files: list[django.core.files.uploadedfile.InMemoryUploadedFile]) | ['@staticmethod', '@permission_classes((IsAuthenticated, ChangeValue))'] |           |

## Класс UnloadFileValueArchiveMutation

Выгрузка архива значения ячейки типа `Файл`.

### Методы

| Signature                                                                                                                                             | Decorator                                                    | Docstring |
| :---------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, document_id: str, sheet_id: str, column_id: str, row_id: str, name: str) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

## Класс ValueMutations

Мутации, связанные с ячейками.