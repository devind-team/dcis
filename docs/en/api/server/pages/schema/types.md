# Модуль types



## Класс CategoryType

Категория

### Методы

| Сигнатура                                                                                                                   | Декораторы                                                     | Описание                                                     |
| :-------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------- | :----------------------------------------------------------- |
| resolve_children( category: apps.pages.models.category.Category, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['staticmethod', "resolver_hints(model_field='category_set')"] | -                                                            |
| resolve_nc( category: apps.pages.models.category.Category, info: graphql.execution.base.ResolveInfo, *args, **kwargs)       | ['staticmethod']                                               | Вытягивает соседей если нет родителей или дочерние элементы. |
| resolve_pages( category: apps.pages.models.category.Category, info: graphql.execution.base.ResolveInfo, *args, **kwargs)    | ['staticmethod', "resolver_hints(model_field='page_set')"]     | -                                                            |

## Класс TagType

Тег

## Класс PageKindType

Тип страницы

### Методы

| Сигнатура                                                                                                                        | Декораторы                                                           | Описание |
| :------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------- | :------- |
| resolve_segment_elements( kind: apps.pages.models.page_kind.PageKind, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['staticmethod', "resolver_hints(model_field='segmentelement_set')"] | -        |
| resolve_pages( kind: apps.pages.models.page_kind.PageKind, info: graphql.execution.base.ResolveInfo, *args, **kwargs)            | ['staticmethod', "resolver_hints(model_field='page_set')"]           | -        |
| resolve_name(model, info: graphql.execution.base.ResolveInfo)                                                                    | -                                                                    | -        |

## Класс PageType

Страница

### Методы

| Сигнатура                                                                                                                           | Декораторы                                                    | Описание |
| :---------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ | :------- |
| resolve_sections( page: apps.pages.models.page.Page, info: graphql.execution.base.ResolveInfo, *args, **kwargs)                     | ['staticmethod', "resolver_hints(model_field='section_set')"] | -        |
| resolve_tags( page: apps.pages.models.page.Page, info: graphql.execution.base.ResolveInfo, *args, **kwargs)                         | ['staticmethod', "resolver_hints(model_field='tags')"]        | -        |
| resolve_comments( page: apps.pages.models.page.Page, info: graphql.execution.base.ResolveInfo, *args, **kwargs)                     | ['staticmethod', "resolver_hints(model_field='comment_set')"] | -        |
| resolve_preview( page: apps.pages.models.page.Page, info: graphql.execution.base.ResolveInfo, *args, **kwargs) -&#62; Optional[str] | ['staticmethod']                                              | -        |

## Класс SectionInterface

Interface Type Definition When a field can return one of a heterogeneous set of types, a Interface type is used to describe what types are possible, what fields are in common across all types, as well as a function to determine which type is actually used when the field is resolved. .. code:: python from graphene import Interface, String class HasAddress(Interface): class Meta: description = "Address fields" address1 = String() address2 = String() If a field returns an Interface Type, the ambiguous type of the object can be determined using ``resolve_type`` on Interface and an ObjectType with ``Meta.possible_types`` or ``is_type_of``. Meta: name (str): Name of the GraphQL type (must be unique in schema). Defaults to class name. description (str): Description of the GraphQL type in the schema. Defaults to class docstring. fields (Dict[str, graphene.Field]): Dictionary of field name to Field. Not recommended to use (prefer class attributes).

### Методы

| Сигнатура                                                                                                | Декораторы      | Описание |
| :------------------------------------------------------------------------------------------------------- | :-------------- | :------- |
| resolve_type( cls, section: apps.pages.models.section.Section, info: graphql.execution.base.ResolveInfo) | ['classmethod'] | -        |

## Класс SectionTextType

Секции

## Класс SectionFilesType

Оптимизирует запросы переопределяя метод get_queryset Является рабочей копией OptimizedDjangoObjectType из graphene_django_optimizer

### Методы

| Сигнатура                                                                                                             | Декораторы       | Описание |
| :-------------------------------------------------------------------------------------------------------------------- | :--------------- | :------- |
| resolve_files( section: apps.pages.models.section.Section, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['staticmethod'] | -        |

## Класс SectionGalleryType

Оптимизирует запросы переопределяя метод get_queryset Является рабочей копией OptimizedDjangoObjectType из graphene_django_optimizer

### Методы

| Сигнатура                                                                                                              | Декораторы       | Описание |
| :--------------------------------------------------------------------------------------------------------------------- | :--------------- | :------- |
| resolve_images( section: apps.pages.models.section.Section, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['staticmethod'] | -        |

## Класс SectionUsersType

Оптимизирует запросы переопределяя метод get_queryset Является рабочей копией OptimizedDjangoObjectType из graphene_django_optimizer

## Класс CommentType

Комментарии

### Методы

| Сигнатура                                                                                                                | Декораторы                                                    | Описание |
| :----------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ | :------- |
| resolve_children( comment: apps.pages.models.comment.Comment, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['staticmethod', "resolver_hints(model_field='comment_set')"] | -        |

## Класс SegmentType

Сегмент

### Методы

| Сигнатура                                                                                                                | Декораторы                                                           | Описание |
| :----------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------- | :------- |
| resolve_elements( segment: apps.pages.models.segment.Segment, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['staticmethod', "resolver_hints(model_field='segmentelement_set')"] | -        |

## Класс SegmentElementType

Элемент сегмента

### Методы

| Сигнатура                                                                                                                        | Декораторы       | Описание |
| :------------------------------------------------------------------------------------------------------------------------------- | :--------------- | :------- |
| resolve_page_kind( element: apps.pages.models.segment.SegmentElement, info: graphql.execution.base.ResolveInfo, *args, **kwargs) | ['staticmethod'] | -        |