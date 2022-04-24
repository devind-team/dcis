import graphene
from devind_helpers.orm_utils import get_object_or_none
from django.db.models import F
from graphene_django import DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.pages.models import Category, Page, PageKind
from .mutations import CategoryMutations, \
    PageMutations, \
    SectionMutations, \
    TagMutations
from .types import CategoryType, PageKindType, PageType, TagType, CommentType
from .types import SectionTextType, SectionFilesType, SectionUsersType
from .types import SegmentType, SegmentElementType


class Query(graphene.ObjectType):
    """Запросы для приложения pages"""

    category = graphene.Field(
        CategoryType,
        category_id=graphene.ID(required=True),
        required=True,
        description='Категория'
    )
    categories = DjangoFilterConnectionField(CategoryType, required=True, description='Категории')
    page_kind = graphene.Field(PageKindType, page_kind_id=graphene.ID(required=True), required=True, description='Получение типа страницы')
    page_kinds = DjangoListField(PageKindType, required=True, description='Типы страниц')
    page = graphene.Field(PageType, page_id=graphene.ID(required=True), required=True, description='Страница')
    pages = DjangoFilterConnectionField(PageType, required=True, description='Страницы')
    tags = DjangoFilterConnectionField(TagType, required=True, description='Теги')
    segments = DjangoListField(SegmentType, required=True, description='Сегменты страницы')

    @staticmethod
    def resolve_category(root, info: ResolveInfo, category_id: str, *args, **kwargs):
        return get_object_or_none(Category, pk=from_global_id(category_id)[1])

    @staticmethod
    def resolve_page_kind(root, info: ResolveInfo, page_kind_id: str, *args, **kwargs):
        return get_object_or_none(PageKind, pk=page_kind_id)

    @staticmethod
    def resolve_page(root, info: ResolveInfo, page_id: str, *args, **kwargs):
        pk: int = from_global_id(page_id)[1]
        Page.objects.filter(pk=pk).update(views=F('views') + 1)
        return get_object_or_none(Page, pk=pk)


class Mutation(CategoryMutations, PageMutations, SectionMutations, TagMutations, graphene.ObjectType):
    """Мутации для приложения pages"""

    pass


types = [SectionTextType, SectionFilesType, SectionUsersType]
