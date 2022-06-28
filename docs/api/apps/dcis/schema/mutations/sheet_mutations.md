# Модуль sheet_mutations

Описание модуля

# Класс RenameSheetMutation

Описание класса Изменение названия листа. Во время мутации изменяем только формулы и ничего не пересчитываем.

## Методы

| Signature                                                                                              | Decorator                                                                | Docstring |
| :----------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, sheet_id: str, name: str) | ['@staticmethod', '@permission_classes((IsAuthenticated, ChangeSheet))'] |           |

# Класс ChangeColumnDimensionMutation

Описание класса Изменение колонки.

## Методы

| Signature                                                                                                                                                       | Decorator                                                    | Docstring |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, column_dimension_id: str, width: int | None, fixed: bool, hidden: bool, kind: str) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

# Класс AddRowDimensionMutation

Описание класса Добавление строки.

## Методы

| Signature                                                                                                                                                                                                                                       | Decorator                                                    | Docstring |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, document_id: str | None, sheet_id: int, parent_id: str | None, index: int, global_index: int, global_indices: list[apps.dcis.schema.types.GlobalIndicesInputType]) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

# Класс ChangeRowDimensionMutation

Описание класса Изменение строки.

## Методы

| Signature                                                                                                                                                         | Decorator                                                    | Docstring |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, row_dimension_id: str, height: int | None, fixed: bool, hidden: bool, dynamic: bool) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

# Класс DeleteRowDimensionMutation

Описание класса Удаление строки.

## Методы

| Signature                                                                                           | Decorator                                                    | Docstring |
| :-------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, row_dimension_id: str) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

# Класс ChangeCellsOptionMutation

Описание класса Изменение свойств ячеек: - strong - true, false - italic - true, false - strike - true, false - underline - [None, 'single', 'double', 'single_accounting', 'double_accounting'] - horizontal_align - ['left', 'center', 'right'] - vertical_align - ['top', 'middle', 'bottom'] - size - число от 6 до 24 - kind - [ 'n', 's', 'f', 'b', 'inlineStr', 'e', 'str', 'd', 'text', 'money', 'bigMoney', 'fl', 'user', 'department', 'organization', 'classification' ]

## Методы

| Signature                                                                                                                               | Decorator                                                    | Docstring |
| :-------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, cell_ids: list[int], field: str, value: str | None = None) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] |           |

# Класс SheetMutations

Описание класса Список мутаций для работы с листами документа.