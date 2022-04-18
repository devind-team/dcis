from typing import List, Optional

import graphene
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.pages.models import Category, Page, PageKind, Tag
from apps.pages.validators import PageValidator
from devind_helpers.schema.types import ErrorFieldType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404, get_object_or_none
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from ..types import PageType
from ...permissions import AddPage, ChangePage, DeletePage


# ---------- Вспомогательные функции ----------

# Временно, лучше дописать функционал проверки массива в валидатор
def check_tag_names(tag_names: List[str]) -> List[ErrorFieldType]:
    return [
        ErrorFieldType('tags', ['Минимальная длина не менее 1 символа'])
        if len(tag_name) < 1 else
        ErrorFieldType('tags', ['Максимальная длина не более 256 символов'])
        for tag_name in tag_names
        if not 1 <= len(tag_name) <= 256
    ]


# ---------- Мутации на добавления страниц ----------

class AddPageMutation(BaseMutation):
    """Добавление страницы"""
    class Input:
        avatar = Upload(description='Аватар')
        parallax = graphene.Boolean(description='Показывать параллакс или нет')
        title = graphene.String(required=True, description='Заголовок')
        signature = graphene.String(description='Подпись страницы')
        hide = graphene.Boolean(description='Скрываем ли страницу')
        priority = graphene.Boolean(description='Приоритет')
        kind_id = graphene.Int(description='Тип страницы')
        category_id = graphene.ID(required=True, description='Категория страницы')
        tag_names = graphene.List(graphene.NonNull(graphene.String), description='Теги на странице')
        text = graphene.String(description='Первоначальное добавление текста страницы')

    page = graphene.Field(PageType, description='Добавленная страница')

    @staticmethod
    @permission_classes([IsAuthenticated, AddPage])
    def mutate_and_get_payload(root, info: ResolveInfo, text: Optional[str], *args, **kwargs):
        data = Page.resolve_global({**kwargs, 'user_id': info.context.user.pk})
        validator: PageValidator = PageValidator(data)
        if validator.validate():
            tag_names = data.pop('tag_names', [])
            errors: List[ErrorFieldType] = check_tag_names(tag_names)
            if len(errors) != 0:
                return AddPageMutation(success=False, errors=errors)
            tags: List[Tag] = [
                Tag.objects.get_or_create(name=tag_name, defaults={'user': info.context.user})[0]
                for tag_name in tag_names
            ]
            page: Page = Page.objects.create(**data)
            page.tags.set(tags)
            if text:
                page.section_set.create(text=text, user=info.context.user)
            return AddPageMutation(page=page)
        return AddPageMutation(success=False, errors=ErrorFieldType.from_validator(validator.get_message()))


# ---------- Мутации на изменение страниц ----------

class ChangePageMutation(BaseMutation):
    """Обобщенная мутация для возвращения измененной страницы"""
    class Meta:
        abstract = True

    page = graphene.Field(PageType, description='Измененная страница')

    @staticmethod
    def get_page(info: ResolveInfo, page_id: str) -> Page:
        page_id = from_global_id(page_id)[1]
        page: Page = get_object_or_404(Page, pk=page_id)
        info.context.check_object_permissions(info.context, page)
        return page


class ChangePageAvatarMutation(ChangePageMutation):
    """Изменение аватара на странице"""
    class Input:
        page_id = graphene.ID(required=True, description='Идентификатор страницы')
        avatar = Upload(description='Новый аватар страницы')

    @staticmethod
    @permission_classes([IsAuthenticated, ChangePage])
    def mutate_and_get_payload(root, info: ResolveInfo, page_id: str, avatar: InMemoryUploadedFile or None,
                               *args, **kwargs):
        page: Page = ChangePageMutation.get_page(info, page_id)
        page.avatar = avatar
        page.save(update_fields=('avatar',))
        return ChangePageAvatarMutation(page=page)


class ChangePageBooleanPropertyMutation(ChangePageMutation):
    """Изменение boolean свойств страницы"""
    class Input:
        page_id = graphene.ID(required=True, description='Идентификатор страницы')
        field = graphene.String(required=True, desctiption='Название поля')
        value = graphene.Boolean(required=True, description='Значение')

    @staticmethod
    @permission_classes([IsAuthenticated, ChangePage])
    def mutate_and_get_payload(root, info: ResolveInfo, page_id: str, field: str, value: bool, *args, **kwargs):
        page: Page = ChangePageMutation.get_page(info, page_id)
        if not hasattr(page, field) or not isinstance(getattr(page, field), bool):
            return ChangePageBooleanPropertyMutation(
                success=False,
                errors=[ErrorFieldType(field, [f'Поле {field} не обнаружено'])]
            )
        setattr(page, field, value)
        page.save(update_fields=(field,))
        return ChangePageBooleanPropertyMutation(page=page)


class ChangePageTitleMutation(ChangePageMutation):
    """Изменение названия страницы"""
    class Input:
        page_id = graphene.ID(required=True, description='Идентификатор страницы')
        title = graphene.String(required=True, description='Заголовок страницы')

    @staticmethod
    @permission_classes([IsAuthenticated, ChangePage])
    def mutate_and_get_payload(root, info: ResolveInfo, page_id: str, title: str, *args, **kwargs):
        page: Page = ChangePageMutation.get_page(info, page_id)
        validator: PageValidator = PageValidator({'title': title})
        if validator.validate():
            page.title = title
            page.save(update_fields=('title',))
            return ChangePageTitleMutation(page=page)
        else:
            return ChangePageTitleMutation(success=False, errors=ErrorFieldType.from_validator(validator.get_message()))


class ChangePageTagsMutation(ChangePageMutation):
    """Изменения тегов страницы"""
    class Input:
        page_id = graphene.ID(required=True, description='Идентификатор страницы')
        tag_names = graphene.List(graphene.NonNull(graphene.String), required=True, description='Теги')

    @staticmethod
    @permission_classes([IsAuthenticated, ChangePage])
    def mutate_and_get_payload(root, info: ResolveInfo, page_id: str, tag_names: List[str], *args, **kwargs):
        page: Page = ChangePageMutation.get_page(info, page_id)
        errors: List[ErrorFieldType] = check_tag_names(tag_names)
        if len(errors) != 0:
            return ChangePageTagsMutation(success=False, errors=errors)
        tags: List[Tag] = [
            Tag.objects.get_or_create(name=tag_name, defaults={'user': info.context.user})[0]
            for tag_name in tag_names
        ]
        page.tags.set(tags)
        return ChangePageTagsMutation(page=page)


class ChangePageCategoryMutation(ChangePageMutation):
    """Изменение категории страницы"""
    class Input:
        page_id = graphene.ID(required=True, description='Идентификатор страницы')
        category_id = graphene.ID(required=True, description='Идентификатор категории')

    @permission_classes([IsAuthenticated, ChangePage])
    def mutate_and_get_payload(self, root, info: ResolveInfo, page_id: str, category_id: int, *args, **kwargs):
        page: Page = self.get_page(info, page_id)
        category: Category or None = get_object_or_none(Category, pk=from_global_id(category_id)[1])
        if category is None:
            return ChangePageMutation(success=False, errors=[ErrorFieldType('category_id', ['Категория не найдена'])])
        page.category = category
        page.save(update_fields=('category',))
        return ChangePageMutation(page=page)


class ChangePageKindMutation(ChangePageMutation):
    """Изменение типа страницы"""
    class Input:
        page_id = graphene.ID(required=True, description='Идентификатор страницы')
        page_kind_id = graphene.Int(description='Идентификатор типа страницы')

    @staticmethod
    @permission_classes([IsAuthenticated, ChangePage])
    def mutate_and_get_payload(root, info: ResolveInfo, page_id: str, page_kind_id: int or None, *args, **kwargs):
        page: Page = ChangePageMutation.get_page(info, page_id)
        page_kind: PageKind or None = get_object_or_none(PageKind, pk=page_kind_id)
        page.kind = page_kind
        page.save(update_fields=('kind',))
        return ChangePageKindMutation(page=page)


# ---------- Мутации на удаление страниц ----------

class DeletePageMutation(BaseMutation):
    """Удаление страницы"""
    class Input:
        page_id = graphene.ID(required=True, desctiption='Идентификатор страницы')

    @staticmethod
    @permission_classes([IsAuthenticated, DeletePage])
    def mutate_and_get_payload(root, info: ResolveInfo, page_id: str, *args, **kwargs):
        page = get_object_or_none(Page, pk=from_global_id(page_id)[1])
        if page is None:
            return DeletePageMutation(
                success=False,
                errors=[ErrorFieldType('page_id', [f'Такой страницы {page_id} не существует'])]
            )
        info.context.check_object_permissions(info.context, page)
        page.delete()
        return DeletePageMutation()


class PageMutations(graphene.ObjectType):
    add_page = AddPageMutation.Field(required=True)
    change_page_avatar = ChangePageAvatarMutation.Field(required=True)
    change_page_boolean_property = ChangePageBooleanPropertyMutation.Field(required=True)
    change_page_title = ChangePageTitleMutation.Field(required=True)
    change_page_tags = ChangePageTagsMutation.Field(required=True)
    change_page_category = ChangePageCategoryMutation.Field(required=True)
    change_page_kind = ChangePageKindMutation.Field(required=True)
    delete_page = DeletePageMutation.Field(required=True)
