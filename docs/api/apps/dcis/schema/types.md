# Модуль types

Описание модуля

# Класс ProjectType

Описание класса Тип модели проектов.

## Методы

| Signature                                                                                             | Decorator                                                      | Docstring |
| :---------------------------------------------------------------------------------------------------- | :------------------------------------------------------------- | :-------- |
| resolve_periods( project: apps.dcis.models.project.Project, info: graphql.execution.base.ResolveInfo) | ['@staticmethod', "@resolver_hints(model_field='period_set')"] |           |

# Класс PeriodType

Описание класса Тип периода.

## Методы

| Signature                                                                                                                  | Decorator                                                        | Docstring |
| :------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------- | :-------- |
| resolve_documents( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo, *args, **kwargs)     | ['@staticmethod', "@resolver_hints(model_field='document_set')"] |           |
| resolve_divisions( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo, *args, **kwargs)     | ['@staticmethod', "@resolver_hints(model_field='')"]             |           |
| resolve_period_groups( period: apps.dcis.models.project.Period, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['@staticmethod', "@resolver_hints(model_field='')"]             |           |

# Класс DivisionType

Описание класса Список участвующих дивизионов в сборе.

# Класс DivisionModelType

Описание класса Описание обобщенного типа дивизиона.

# Класс OrganizationOriginalType

Описание класса Описание списка организаций.

## Методы

| Signature                                                                                                                                                                               | Decorator                                            | Docstring |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- | :-------- |
| resolve_departments( organization: devind_dictionaries.models.organizations.Organization, info: graphql.execution.base.ResolveInfo, *args, **kwargs) -> django.db.models.query.QuerySet | ['@staticmethod', "@resolver_hints(model_field='')"] |           |

# Класс PrivilegeType

Описание класса Описание сквозных привилегий.

# Класс PeriodGroupType

Описание класса Группы с содержанием привилегий.

## Методы

| Signature                                                                                                                       | Decorator                                            | Docstring |
| :------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------- | :-------- |
| resolve_users( period_group: apps.dcis.models.privilege.PeriodGroup, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['@staticmethod', "@resolver_hints(model_field='')"] |           |

# Класс PeriodPrivilegeType

Описание класса Тип для отдельных привилегий пользователей.

# Класс StatusType

Описание класса Тип статусов документов.

# Класс DocumentType

Описание класса Тип моделей документа.

## Методы

| Signature                                                                                                    | Decorator         | Docstring |
| :----------------------------------------------------------------------------------------------------------- | :---------------- | :-------- |
| resolve_sheets( document: apps.dcis.models.document.Document, info: graphql.execution.base.ResolveInfo)      | ['@staticmethod'] |           |
| resolve_last_status( document: apps.dcis.models.document.Document, info: graphql.execution.base.ResolveInfo) | ['@staticmethod'] |           |

# Класс DocumentStatusType

Описание класса Тип статусов для документов.

# Класс AttributeType

Описание класса Тип атрибутов для документов.

## Методы

| Signature                                                                                                                    | Decorator                                                         | Docstring |
| :--------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------- | :-------- |
| resolve_children( attribute: apps.dcis.models.document.Attribute, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['@staticmethod', "@resolver_hints(model_field='attribute_set')"] |           |

# Класс AttributeValueType

Описание класса Тип со значениями атрибутов.

# Класс ColumnDimensionType

Описание класса Тип колонки.

# Класс RowDimensionType

Описание класса Тип строки.

# Класс CellType

Описание класса Тип ячейки.

# Класс SheetType

Описание класса Тип листа.

# Класс LimitationType

Описание класса Ограничения на ячейку.

# Класс ChangedCellOption

Описание класса Измененное свойство ячейки.

# Класс GlobalIndicesInputType

Описание класса Индекс строки в плоской структуре.