# Модуль types



## Класс ProjectType

Тип модели проектов.

### Методы

| Сигнатура                                                                                                                                    | Декораторы                                             | Описание |
| :------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------- | :------- |
| resolve_periods( project: apps.dcis.models.project.Project, info: graphql.execution.base.ResolveInfo) -&#62; django.db.models.query.QuerySet | staticmethod, resolver_hints(model_field='period_set') | -        |
| resolve_can_change( project: apps.dcis.models.project.Project, info: graphql.execution.base.ResolveInfo) -&#62; bool                         | staticmethod                                           | -        |
| resolve_can_delete( project: apps.dcis.models.project.Project, info: graphql.execution.base.ResolveInfo) -&#62; bool                         | staticmethod                                           | -        |
| resolve_can_add_period( project: apps.dcis.models.project.Project, info: graphql.execution.base.ResolveInfo) -&#62; bool                     | staticmethod                                           | -        |

## Класс PeriodType

Тип периода.

### Методы

| Сигнатура                                                                                                                                    | Декораторы                                                  | Описание |
| :------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------- | :------- |
| resolve_divisions( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo) -&#62; list[dict[str, int &#124; str]] | staticmethod, resolver_hints(model_field='division_set')    | -        |
| resolve_period_groups( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo)                                    | staticmethod, resolver_hints(model_field='periodgroup_set') | -        |
| resolve_can_change_divisions( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo) -&#62; bool                 | staticmethod                                                | -        |
| resolve_can_change_groups( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo) -&#62; bool                    | staticmethod                                                | -        |
| resolve_can_change_users( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo) -&#62; bool                     | staticmethod                                                | -        |
| resolve_can_change_settings( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo) -&#62; bool                  | staticmethod                                                | -        |
| resolve_can_change_sheet( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo) -&#62; bool                     | staticmethod                                                | -        |
| resolve_can_delete( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo) -&#62; bool                           | staticmethod                                                | -        |
| resolve_can_add_document( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo) -&#62; bool                     | staticmethod                                                | -        |

## Класс DivisionModelType

Описание обобщенного типа дивизиона.

## Класс OrganizationOriginalType

Описание списка организаций.

### Методы

| Сигнатура                                                                                                                                                                                   | Декораторы                                   | Описание |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------- | :------- |
| resolve_departments( organization: devind_dictionaries.models.organizations.Organization, info: graphql.execution.base.ResolveInfo, *args, **kwargs) -&#62; django.db.models.query.QuerySet | staticmethod, resolver_hints(model_field='') | -        |

## Класс PrivilegeType

Описание сквозных привилегий.

## Класс PeriodGroupType

Группы с содержанием привилегий.

### Методы

| Сигнатура                                                                                                                                                              | Декораторы                                   | Описание |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------- | :------- |
| resolve_users( period_group: apps.dcis.models.privilege.PeriodGroup, info: graphql.execution.base.ResolveInfo, *args, **kwargs) -&#62; django.db.models.query.QuerySet | staticmethod, resolver_hints(model_field='') | -        |

## Класс PeriodPrivilegeType

Тип для отдельных привилегий пользователей.

## Класс StatusType

Тип статусов документов.

## Класс DocumentType

Тип моделей документа.

### Методы

| Сигнатура                                                                                                                                                                | Декораторы   | Описание |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- | :------- |
| resolve_sheets( document: apps.dcis.models.document.Document, info: graphql.execution.base.ResolveInfo) -&#62; list[dict] &#124; dict                                    | staticmethod | -        |
| resolve_last_status( document: apps.dcis.models.document.Document, info: graphql.execution.base.ResolveInfo) -&#62; apps.dcis.models.document.DocumentStatus &#124; None | staticmethod | -        |
| resolve_can_change( document: apps.dcis.models.document.Document, info: graphql.execution.base.ResolveInfo) -&#62; bool                                                  | staticmethod | -        |
| resolve_can_delete( document: apps.dcis.models.document.Document, info: graphql.execution.base.ResolveInfo) -&#62; bool                                                  | staticmethod | -        |

## Класс DocumentStatusType

Тип статусов для документов.

## Класс AttributeType

Тип атрибутов для документов.

### Методы

| Сигнатура                                                                                                                    | Декораторы                                                | Описание |
| :--------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------- | :------- |
| resolve_children( attribute: apps.dcis.models.document.Attribute, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | staticmethod, resolver_hints(model_field='attribute_set') | -        |

## Класс AttributeValueType

Тип со значениями атрибутов.

## Класс ColumnDimensionType

Тип колонки.

## Класс RowDimensionType

Тип строки.

## Класс CellType

Тип ячейки.

## Класс ValueType

Тип значений

### Методы

| Сигнатура                                                                                                  | Декораторы   | Описание |
| :--------------------------------------------------------------------------------------------------------- | :----------- | :------- |
| resolve_payload( value: apps.dcis.models.sheet.Value, info: graphql.execution.base.ResolveInfo) -&#62; str | staticmethod | -        |

## Класс SheetType

Тип листа.

## Класс LimitationType

Ограничения на ячейку.

## Класс ChangedCellOption

Измененное свойство ячейки.

## Класс GlobalIndicesInputType

Индекс строки в плоской структуре.