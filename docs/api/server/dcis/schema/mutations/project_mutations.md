# Модуль project_mutations



## Класс AddProjectMutationPayload

Мутация для добавления проекта.

### Методы

| Сигнатура                                                                                                    | Декораторы  | Описание |
| :----------------------------------------------------------------------------------------------------------- | :---------- | :------- |
| validate( cls, root: Any, info: graphql.execution.base.ResolveInfo, input, *args, **kwargs)                  | classmethod | -        |
| handle_content_type( cls, value: str, field: str, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | classmethod | -        |

## Класс ChangeProjectMutationPayload

Мутация изменения настроек проекта.

### Методы

| Сигнатура                                                                                                                                            | Декораторы  | Описание |
| :--------------------------------------------------------------------------------------------------------------------------------------------------- | :---------- | :------- |
| check_permissions( cls, root: Any, info: graphql.execution.base.ResolveInfo, input: Any, id: str, obj: apps.dcis.models.project.Project) -&#62; None | classmethod | -        |

## Класс DeleteProjectMutationPayload

Мутация на удаление проекта.

### Методы

| Сигнатура                                                                                                                                | Декораторы  | Описание |
| :--------------------------------------------------------------------------------------------------------------------------------------- | :---------- | :------- |
| check_permissions( cls, root: Any, info: graphql.execution.base.ResolveInfo, id: str, obj: apps.dcis.models.project.Project) -&#62; None | classmethod | -        |

## Класс ProjectMutations

Список мутация проекта.