# Модуль document_mutations



## Класс AddDocumentMutation

Добавление документа.

### Методы

| Сигнатура                                                                                                                                                                                                                                                                      | Декораторы                                                       | Описание                          |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------- | :-------------------------------- |
| mutate_and_get_payload( root: None, info: graphql.execution.base.ResolveInfo, comment: str, period_id: str, status_id: int, document_id: int &#124; None = None, division_id: int &#124; None = None) -&#62; apps.dcis.schema.mutations.document_mutations.AddDocumentMutation | staticmethod, permission_classes((IsAuthenticated, AddDocument)) | Мутация для добавления документа. |

## Класс ChangeDocumentCommentMutationPayload

Изменение комментария версии документа.

### Методы

| Сигнатура                                                                                                                                              | Декораторы  | Описание |
| :----------------------------------------------------------------------------------------------------------------------------------------------------- | :---------- | :------- |
| check_permissions( cls, root: Any, info: graphql.execution.base.ResolveInfo, input: Any, id: str, obj: apps.dcis.models.document.Document) -&#62; None | classmethod | -        |

## Класс AddDocumentStatusMutation

Добавление статуса документа.

### Методы

| Сигнатура                                                                                                                     | Декораторы                                                          | Описание |
| :---------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------ | :------- |
| mutate_and_get_payload( root: None, info: graphql.execution.base.ResolveInfo, document_id: str, status_id: int, comment: str) | staticmethod, permission_classes((IsAuthenticated, ChangeDocument)) | -        |

## Класс DeleteDocumentStatusMutation

Удаление статуса документа.

### Методы

| Сигнатура                                                                                              | Декораторы                                                          | Описание |
| :----------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------ | :------- |
| mutate_and_get_payload( root: None, info: graphql.execution.base.ResolveInfo, document_status_id: int) | staticmethod, permission_classes((IsAuthenticated, ChangeDocument)) | -        |

## Класс UnloadDocumentMutation

Выгрузка документа.

### Методы

| Сигнатура                                                                                                                                 | Декораторы                                           | Описание |
| :---------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- | :------- |
| mutate_and_get_payload( root: None, info: graphql.execution.base.ResolveInfo, document_id: str, additional: list[str] &#124; None = None) | staticmethod, permission_classes((IsAuthenticated,)) | -        |

## Класс DocumentMutations

Мутации, связанные с документами.