# Модуль sheet_mutations



## Класс RenameSheetMutation

Изменение названия листа. Во время мутации изменяем только формулы и ничего не пересчитываем.

### Методы

| Сигнатура                                                                                              | Декораторы                                                             | Описание |
| :----------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, sheet_id: str, name: str) | staticmethod, permission_classes((IsAuthenticated, ChangePeriodSheet)) | -        |

## Класс ChangeColumnDimensionMutation

Изменение колонки.

### Методы

| Сигнатура                                                                                                                                                            | Декораторы                                           | Описание |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, column_dimension_id: str, width: int &#124; None, fixed: bool, hidden: bool, kind: str) | staticmethod, permission_classes((IsAuthenticated,)) | -        |

## Класс AddRowDimensionMutation

Добавление строки.

### Методы

| Сигнатура                                                                                                                                                                                                                                                 | Декораторы                                           | Описание |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, document_id: str &#124; None, sheet_id: int, parent_id: str &#124; None, index: int, global_index: int, global_indices: list[apps.dcis.schema.types.GlobalIndicesInputType]) | staticmethod, permission_classes((IsAuthenticated,)) | -        |

## Класс ChangeRowDimensionMutation

Изменение строки.

### Методы

| Сигнатура                                                                                                                                                              | Декораторы                                           | Описание |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, row_dimension_id: str, height: int &#124; None, fixed: bool, hidden: bool, dynamic: bool) | staticmethod, permission_classes((IsAuthenticated,)) | -        |

## Класс DeleteRowDimensionMutation

Удаление строки.

### Методы

| Сигнатура                                                                                           | Декораторы                                           | Описание |
| :-------------------------------------------------------------------------------------------------- | :--------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, row_dimension_id: str) | staticmethod, permission_classes((IsAuthenticated,)) | -        |

## Класс ChangeCellsOptionMutation

Изменение свойств ячеек: - strong - true, false - italic - true, false - strike - true, false - underline - [None, 'single', 'double', 'single_accounting', 'double_accounting'] - horizontal_align - ['left', 'center', 'right'] - vertical_align - ['top', 'middle', 'bottom'] - size - число от 6 до 24 - kind - [ 'n', 's', 'f', 'b', 'inlineStr', 'e', 'str', 'd', 'text', 'money', 'bigMoney', 'fl', 'user', 'department', 'organization', 'classification' ]

### Методы

| Сигнатура                                                                                                                                    | Декораторы                                           | Описание |
| :------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- | :------- |
| mutate_and_get_payload( root: Any, info: graphql.execution.base.ResolveInfo, cell_ids: list[int], field: str, value: str &#124; None = None) | staticmethod, permission_classes((IsAuthenticated,)) | -        |

## Класс SheetMutations

Список мутаций для работы с листами документа.