from typing import Optional

import graphene
from django.conf import settings
from django.utils.html import strip_tags
from graphene.relay import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django_optimizer.resolver import resolver_hints
from graphql import ResolveInfo

from apps.core.schema import UserType
from devind_core.models import File
from devind_core.schema.connections.countable_connection import CountableConnection
from devind_core.schema.types import FileType, OptimizedDjangoObjectType
from ..decorators import translate_type
from ..models import Category, Page, PageKind, Tag, Comment, Section, Segment, SegmentElement


class CategoryType(OptimizedDjangoObjectType):
    """Категория"""

    parent = graphene.Field(lambda: CategoryType, description='Родительская категория')
    children = graphene.List(lambda: CategoryType, required=True, description='Дочерние категории')
    user = graphene.Field(UserType, description='Пользователь')
    pages = DjangoFilterConnectionField(lambda: PageType, description='Страницы')
    nc = graphene.List(lambda: CategoryType, required=True, description='Соседние категории')

    class Meta:
        model = Category
        interfaces = (Node,)
        fields = (
            'id',
            'avatar',
            'text',
            'position',
            'created_at',
            'updated_at',
            'parent',
            'children',
            'user',
            'pages',
        )
        filter_fields = {
            'text': ['icontains'],
            'parent': ['exact', 'isnull']
        }
        connection_class = CountableConnection

    @staticmethod
    @resolver_hints(model_field='category_set')
    def resolve_children(category: Category, info: ResolveInfo, *args, **kwargs):
        return category.category_set.all()

    @staticmethod
    def resolve_nc(category: Category, info: ResolveInfo, *args, **kwargs):
        """Вытягивает соседей если нет родителей или дочерние элементы."""

        return category.category_set.all() if category.parent is None else category.parent.category_set.all()

    @staticmethod
    @resolver_hints(model_field='page_set')
    def resolve_pages(category: Category, info: ResolveInfo, *args, **kwargs):
        return category.page_set.all()


class TagType(OptimizedDjangoObjectType):
    """Тег"""

    user = graphene.Field(UserType, required=False, description='Пользователь, создавший тег')

    class Meta:
        model = Tag
        interfaces = (Node,)
        fields = (
            'id',
            'name',
            'created_at',
            'user',
        )
        filter_fields = {'name': ['icontains']}
        connection_class = CountableConnection


@translate_type(['name'])
class PageKindType(OptimizedDjangoObjectType):
    """Тип страницы"""

    pages = graphene.List(lambda: PageType, required=True, description='Странички')
    segment_elements = graphene.List(lambda: SegmentElementType, required=True, description='Сегментные элементы')

    class Meta:
        model = PageKind
        fields = (
            'id',
            'name',
            'pages',
            'segment_elements'
        )

    @staticmethod
    @resolver_hints(model_field='segmentelement_set')
    def resolve_segment_elements(kind: PageKind, info: ResolveInfo, *args, **kwargs):
        return kind.segmentelement_set.all()

    @staticmethod
    @resolver_hints(model_field='page_set')
    def resolve_pages(kind: PageKind, info: ResolveInfo, *args, **kwargs):
        page_size = info.context.page_size if hasattr(info.context, 'page_size') else settings.DEFAULT_PAGE_SIZE
        return kind.page_set.all()[:page_size]


class PageType(OptimizedDjangoObjectType):
    """Страница"""

    category = graphene.Field(CategoryType, required=True, description='Категория')
    tags = graphene.List(TagType, required=True, description='Теги на странице')
    sections = graphene.List(lambda: SectionInterface, required=True, description='Секции')
    comments = DjangoFilterConnectionField(lambda: CommentType, required=True, description='Комментарии')

    kind = graphene.Field(PageKindType, description='Тип')
    user = graphene.Field(UserType, description='Пользователь, создавший страницу')
    preview = graphene.String(description='Первая текстовая секция')

    class Meta:
        model = Page
        interfaces = (Node,)
        filter_fields = {
            'title': ['icontains'],
            'kind__id': ['exact'],
            'category__id': ['exact']
        }
        connection_class = CountableConnection
        fields = (
            'id',
            'avatar',
            'parallax',
            'title',
            'views',
            'signature',
            'hide',
            'priority',
            'created_at',
            'updated_at',
            'category',
            'tags',
            'sections',
            'comments',
            'kind',
            'user',
            'preview'
        )

    @staticmethod
    @resolver_hints(model_field='section_set')
    def resolve_sections(page: Page, info: ResolveInfo, *args, **kwargs):
        return page.section_set.all()

    @staticmethod
    @resolver_hints(model_field='tags')
    def resolve_tags(page: Page, info: ResolveInfo, *args, **kwargs):
        return page.tags.all()

    @staticmethod
    @resolver_hints(model_field='comment_set')
    def resolve_comments(page: Page, info: ResolveInfo, *args, **kwargs):
        return page.comment_set.all()

    @staticmethod
    def resolve_preview(page: Page, info: ResolveInfo, *args, **kwargs) -> Optional[str]:
        section = page.section_set.filter(kind=Section.TEXT).order_by('position').first()
        if section:
            text: str = strip_tags(section.text)[:220]
            text: str = ".".join(text.split(".")[:-1])
            return f'{text}...' if len(text) > 5 else None
        return None


class SectionInterface(graphene.Interface):

    id = graphene.Int(required=True, description='Идентификатор')
    text = graphene.String(required=True, description='Текст страницы')
    kind = graphene.Int(required=True, description='Тип страницы')
    position = graphene.Int(required=True, description='Порядок вывода')
    page = graphene.Field(PageType, required=True, description='Страница')
    user = graphene.Field(UserType, required=True, description='Пользователь')

    @classmethod
    def resolve_type(cls, section: Section, info: ResolveInfo):
        resolver = {
            section.TEXT: SectionTextType,
            section.FILES: SectionFilesType,
            section.USERS: SectionUsersType,
            section.GALLERY: SectionGalleryType
        }
        return resolver.get(section.kind, SectionTextType)


class SectionTextType(OptimizedDjangoObjectType):
    """Секции"""

    class Meta:
        model = Section
        fields = (
            'id',
            'text',
            'kind',
            'position',
            'page',
            'user',
        )
        interfaces = (SectionInterface,)


class SectionFilesType(OptimizedDjangoObjectType):
    files = graphene.List(FileType, required=True, description='Файлы')

    class Meta:
        model = Section
        fields = (
            'id',
            'text',
            'kind',
            'payload',
            'position',
            'page',
            'user',
        )
        interfaces = (SectionInterface,)

    @staticmethod
    def resolve_files(section: Section, info: ResolveInfo, *args, **kwargs):
        return File.objects.filter(pk__in=section.payload['files']) if 'files' in section.payload else []


class SectionGalleryType(OptimizedDjangoObjectType):
    images = graphene.List(FileType, required=True, description='Изображения')

    class Meta:
        model = Section
        fields = (
            'id',
            'text',
            'kind',
            'position',
            'payload',
            'page',
            'user',
        )
        interfaces = (SectionInterface,)

    @staticmethod
    def resolve_images(section: Section, info: ResolveInfo, *args, **kwargs):
        return File.objects.filter(pk__in=section.payload['images']) if 'images' in section.payload else []


class SectionUsersType(OptimizedDjangoObjectType):
    users = graphene.List(UserType, required=True, description='Пользователи')

    class Meta:
        model = Section
        fields = (
            'id',
            'text',
            'kind',
            'payload',
            'position',
            'page',
            'user',
            'users',
        )
        interfaces = (SectionInterface,)


class CommentType(OptimizedDjangoObjectType):
    """Комментарии"""

    children = graphene.List(lambda: CategoryType, required=True, description='Дочерние комментарии')
    page = graphene.Field(PageType, required=True, description='Страница')
    user = graphene.Field(UserType, required=True, description='Пользователь, оставивший комментарий')

    class Meta:
        model = Comment
        interfaces = (Node,)
        fields = (
            'id',
            'text',
            'rating',
            'created_at',
            'updated_at',
            'user',
            'page',
            'children',
        )
        filter_fields = {'text': ['icontains']}
        connection_class = CountableConnection

    @staticmethod
    @resolver_hints(
        model_field='comment_set',
    )
    def resolve_children(comment: Comment, info: ResolveInfo, *args, **kwargs):
        return comment.comment_set.all()


class SegmentType(OptimizedDjangoObjectType):
    """Сегмент"""

    elements = graphene.List(lambda: SegmentElementType, required=True, description='Элементы сегмента страницы')

    class Meta:
        model = Segment
        fields = (
            'id',
            'name',
            'align',
            'view',
            'position',
            'created_at',
            'updated_at',
        )

    @staticmethod
    @resolver_hints(
        model_field='segmentelement_set',
    )
    def resolve_elements(segment: Segment, info: ResolveInfo, *args, **kwargs):
        return segment.segmentelement_set.all()


class SegmentElementType(OptimizedDjangoObjectType):
    """Элемент сегмента"""

    user = graphene.Field(UserType, required=True, description='Пользователь')
    page_kind = graphene.Field(PageKindType, required=True, description='Тип страницы')

    class Meta:
        model = SegmentElement
        fields = (
            'id',
            'view',
            'represent',
            'columns',
            'width',
            'page_size',
            'position',
            'created_at',
            'updated_at',
            'page_kind',
            'user',
        )

    @staticmethod
    def resolve_page_kind(element: SegmentElement, info: ResolveInfo, *args, **kwargs):
        info.context.page_size = element.page_size
        return element.page_kind
