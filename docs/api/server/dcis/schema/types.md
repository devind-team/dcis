# Модуль types



## Класс ProjectType

Тип модели проектов.

### Методы

| Сигнатура                                                                                             | Декораторы                                                   | Описание |
| :---------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :------- |
| resolve_periods( project: apps.dcis.models.project.Project, info: graphql.execution.base.ResolveInfo) | ['staticmethod', "resolver_hints(model_field='period_set')"] | -        |

## Класс PeriodType

Тип периода.

### Методы

| Сигнатура                                                                                                                  | Декораторы                                                     | Описание |
| :------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------- | :------- |
| resolve_documents( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo, *args, **kwargs)     | ['staticmethod', "resolver_hints(model_field='document_set')"] | -        |
| resolve_divisions( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo, *args, **kwargs)     | ['staticmethod', "resolver_hints(model_field='')"]             | -        |
| resolve_period_groups( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['staticmethod', "resolver_hints(model_field='')"]             | -        |

## Класс DivisionType

Список участвующих дивизионов в сборе.

## Класс DivisionModelType

Описание обобщенного типа дивизиона.

## Класс OrganizationOriginalType

Описание списка организаций.

### Методы

| Сигнатура                                                                                                                                                                                   | Декораторы                                         | Описание |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------- | :------- |
| resolve_departments( organization: devind_dictionaries.models.organizations.Organization, info: graphql.execution.base.ResolveInfo, *args, **kwargs) -&#62; django.db.models.query.QuerySet | ['staticmethod', "resolver_hints(model_field='')"] | -        |

## Класс PrivilegeType

Описание сквозных привилегий.

## Класс PeriodGroupType

Группы с содержанием привилегий.

### Методы

| Сигнатура                                                                                                                       | Декораторы                                         | Описание |
| :------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------- | :------- |
| resolve_users( period_group: apps.dcis.models.privilege.PeriodGroup, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['staticmethod', "resolver_hints(model_field='')"] | -        |

## Класс PeriodPrivilegeType

Тип для отдельных привилегий пользователей.

## Класс StatusType

Тип статусов документов.

## Класс DocumentType

Тип моделей документа.

### Методы

| Сигнатура                                                                                                    | Декораторы       | Описание |
| :----------------------------------------------------------------------------------------------------------- | :--------------- | :------- |
| resolve_sheets( document: apps.dcis.models.document.Document, info: graphql.execution.base.ResolveInfo)      | ['staticmethod'] | -        |
| resolve_last_status( document: apps.dcis.models.document.Document, info: graphql.execution.base.ResolveInfo) | ['staticmethod'] | -        |

## Класс DocumentStatusType

Тип статусов для документов.

## Класс AttributeType

Тип атрибутов для документов.

### Методы

| Сигнатура                                                                                                                    | Декораторы                                                      | Описание |
| :--------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------- | :------- |
| resolve_children( attribute: apps.dcis.models.document.Attribute, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['staticmethod', "resolver_hints(model_field='attribute_set')"] | -        |

## Класс AttributeValueType

Тип со значениями атрибутов.

## Класс ColumnDimensionType

Тип колонки.

## Класс RowDimensionType

Тип строки.

## Класс CellType

Тип ячейки.

## Класс SheetType

Тип листа.

## Класс LimitationType

Ограничения на ячейку.

## Класс ChangedCellOption

Измененное свойство ячейки.

## Класс GlobalIndicesInputType

Индекс строки в плоской структуре.