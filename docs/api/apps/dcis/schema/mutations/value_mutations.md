# Модуль value_mutations

Описание модуля Модуль содержит мутации, относящиеся к значениям ячеек.

# Класс ChangeValueMutation

Описание класса Изменение значения ячейки.

## Методы

| Signature                                                                                                                                              | Decorator                                                                | Docstring |
| :----------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, document_id: str, sheet_id: str, column_id: str, row_id: str, value: str) | ['@staticmethod', '@permission_classes((IsAuthenticated, ChangeValue))'] |           |

# Класс ChangeFileValueMutation

Описание класса Изменение значения ячейки типа `Файл`.

## Методы

| Signature                                                                                                                                                                                                                                                | Decorator                                                                | Docstring |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, document_id: str, sheet_id: str, column_id: str, row_id: str, value: str, remaining_files: list[str], new_files: list[django.core.files.uploadedfile.InMemoryUploadedFile]) | ['@staticmethod', '@permission_classes((IsAuthenticated, ChangeValue))'] |           |

# Класс UnloadFileValueArchiveMutation

Описание класса Выгрузка архива значения ячейки типа `Файл`.

## Методы

| Signature                                                                                                                                             | Decorator                                                    | Docstring |
| :---------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, document_id: str, sheet_id: str, column_id: str, row_id: str, name: str) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

# Класс ValueMutations

Описание класса Мутации, связанные с ячейками.