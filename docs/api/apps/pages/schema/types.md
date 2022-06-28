# Модуль types

Описание модуля

# Класс CategoryType

Описание класса Категория

## Методы

| Signature                                                                                                                   | Decorator                                                        | Docstring                                                    |
| :-------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------- | :----------------------------------------------------------- |
| resolve_children( category: apps.pages.models.category.Category, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['@staticmethod', "@resolver_hints(model_field='category_set')"] |                                                              |
| resolve_nc( category: apps.pages.models.category.Category, info: graphql.execution.base.ResolveInfo, *args, **kwargs)       | ['@staticmethod']                                                | Вытягивает соседей если нет родителей или дочерние элементы. |
| resolve_pages( category: apps.pages.models.category.Category, info: graphql.execution.base.ResolveInfo, *args, **kwargs)    | ['@staticmethod', "@resolver_hints(model_field='page_set')"]     |                                                              |

# Класс TagType

Описание класса Тег

# Класс PageKindType

Описание класса Тип страницы

## Методы

| Signature                                                                                                                        | Decorator                                                              | Docstring |
| :------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- | :-------- |
| resolve_segment_elements( kind: apps.pages.models.page_kind.PageKind, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['@staticmethod', "@resolver_hints(model_field='segmentelement_set')"] |           |
| resolve_pages( kind: apps.pages.models.page_kind.PageKind, info: graphql.execution.base.ResolveInfo, *args, **kwargs)            | ['@staticmethod', "@resolver_hints(model_field='page_set')"]           |           |
| resolve_name(model, info: graphql.execution.base.ResolveInfo)                                                                    | -                                                                      |           |

# Класс PageType

Описание класса Страница

## Методы

| Signature                                                                                                                       | Decorator                                                       | Docstring |
| :------------------------------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------- | :-------- |
| resolve_sections( page: apps.pages.models.page.Page, info: graphql.execution.base.ResolveInfo, *args, **kwargs)                 | ['@staticmethod', "@resolver_hints(model_field='section_set')"] |           |
| resolve_tags( page: apps.pages.models.page.Page, info: graphql.execution.base.ResolveInfo, *args, **kwargs)                     | ['@staticmethod', "@resolver_hints(model_field='tags')"]        |           |
| resolve_comments( page: apps.pages.models.page.Page, info: graphql.execution.base.ResolveInfo, *args, **kwargs)                 | ['@staticmethod', "@resolver_hints(model_field='comment_set')"] |           |
| resolve_preview( page: apps.pages.models.page.Page, info: graphql.execution.base.ResolveInfo, *args, **kwargs) -> Optional[str] | ['@staticmethod']                                               |           |

# Класс SectionInterface

Описание класса Interface Type Definition When a field can return one of a heterogeneous set of types, a Interface type is used to describe what types are possible, what fields are in common across all types, as well as a function to determine which type is actually used when the field is resolved. .. code:: python from graphene import Interface, String class HasAddress(Interface): class Meta: description = "Address fields" address1 = String() address2 = String() If a field returns an Interface Type, the ambiguous type of the object can be determined using ``resolve_type`` on Interface and an ObjectType with ``Meta.possible_types`` or ``is_type_of``. Meta: name (str): Name of the GraphQL type (must be unique in schema). Defaults to class name. description (str): Description of the GraphQL type in the schema. Defaults to class docstring. fields (Dict[str, graphene.Field]): Dictionary of field name to Field. Not recommended to use (prefer class attributes).

## Методы

| Signature                                                                                                | Decorator        | Docstring |
| :------------------------------------------------------------------------------------------------------- | :--------------- | :-------- |
| resolve_type( cls, section: apps.pages.models.section.Section, info: graphql.execution.base.ResolveInfo) | ['@classmethod'] |           |

# Класс SectionTextType

Описание класса Секции

# Класс SectionFilesType

Описание класса Оптимизирует запросы переопределяя метод get_queryset Является рабочей копией OptimizedDjangoObjectType из graphene_django_optimizer

## Методы

| Signature                                                                                                             | Decorator         | Docstring |
| :-------------------------------------------------------------------------------------------------------------------- | :---------------- | :-------- |
| resolve_files( section: apps.pages.models.section.Section, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['@staticmethod'] |           |

# Класс SectionGalleryType

Описание класса Оптимизирует запросы переопределяя метод get_queryset Является рабочей копией OptimizedDjangoObjectType из graphene_django_optimizer

## Методы

| Signature                                                                                                              | Decorator         | Docstring |
| :--------------------------------------------------------------------------------------------------------------------- | :---------------- | :-------- |
| resolve_images( section: apps.pages.models.section.Section, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['@staticmethod'] |           |

# Класс SectionUsersType

Описание класса Оптимизирует запросы переопределяя метод get_queryset Является рабочей копией OptimizedDjangoObjectType из graphene_django_optimizer

# Класс CommentType

Описание класса Комментарии

## Методы

| Signature                                                                                                                | Decorator                                                       | Docstring |
| :----------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------- | :-------- |
| resolve_children( comment: apps.pages.models.comment.Comment, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['@staticmethod', "@resolver_hints(model_field='comment_set')"] |           |

# Класс SegmentType

Описание класса Сегмент

## Методы

| Signature                                                                                                                | Decorator                                                              | Docstring |
| :----------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- | :-------- |
| resolve_elements( segment: apps.pages.models.segment.Segment, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['@staticmethod', "@resolver_hints(model_field='segmentelement_set')"] |           |

# Класс SegmentElementType

Описание класса Элемент сегмента

## Методы

| Signature                                                                                                                        | Decorator         | Docstring |
| :------------------------------------------------------------------------------------------------------------------------------- | :---------------- | :-------- |
| resolve_page_kind( element: apps.pages.models.segment.SegmentElement, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['@staticmethod'] |           |