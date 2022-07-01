# Модуль document_mutations



## Класс AddDocumentMutation

Добавление документа.

### Методы

| Signature                                                                                                                                                                                                                                                              | Decorator                                                                | Docstring                       |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------- | :------------------------------ |
| mutate_and_get_payload( root: None, info: graphql.execution.base.ResolveInfo, comment: str, period_id: str, status_id: int, document_id: Optional[int] = None, division_id: Optional[int] = None) -> apps.dcis.schema.mutations.document_mutations.AddDocumentMutation | ['@staticmethod', '@permission_classes((IsAuthenticated, AddDocument))'] | Мутация для создания документа. |

## Класс ChangeDocumentCommentMutationPayload

Изменение комментария версии документа.

## Класс AddDocumentStatusMutation

Добавление статуса документа.

### Методы

| Signature                                                                                                                     | Decorator                                                                      | Docstring |
| :---------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: None, info: graphql.execution.base.ResolveInfo, document_id: str, status_id: int, comment: str) | ['@staticmethod', '@permission_classes((IsAuthenticated, AddDocumentStatus))'] | -         |

## Класс DeleteDocumentStatusMutation

Удаление статуса документа.

### Методы

| Signature                                                                                                               | Decorator                                                                         | Docstring |
| :---------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: None, info: graphql.execution.base.ResolveInfo, document_status_id: int, *args, **kwargs) | ['@staticmethod', '@permission_classes((IsAuthenticated, DeleteDocumentStatus))'] | -         |

## Класс UnloadDocumentMutation

Выгрузка документа.

### Методы

| Signature                                                                                                                               | Decorator                                                    | Docstring |
| :-------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :-------- |
| mutate_and_get_payload( root: None, info: graphql.execution.base.ResolveInfo, document_id: str, additional: Optional[list[str]] = None) | ['@staticmethod', '@permission_classes((IsAuthenticated,))'] | -         |

## Класс DocumentMutations

Мутации, связанные с документами.