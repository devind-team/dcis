from typing import List

import graphene
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.db.models import Max
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.pages.models import Category
from apps.pages.validators import CategoryValidator
from devind_helpers.schema.types import ErrorFieldType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404, get_object_or_none
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from ..types import CategoryType
from ...permissions import AddCategory, ChangeAbsoluteCategory, ChangeCategory, DeleteCategory


class AddCategoryMutation(BaseMutation):
    """Мутация для добавления категории"""
    class Input:
        avatar = Upload(description='Аватар')
        text = graphene.String(required=True, description='Название категории')
        parent_id = graphene.ID(description='Идентификатор родительской категории')

    category = graphene.Field(CategoryType, description='Добавленная котегория')

    @staticmethod
    @permission_classes([IsAuthenticated, AddCategory])
    def mutate_and_get_payload(root, info: ResolveInfo, *args, **kwargs):
        data = Category.resolve_global({**kwargs, 'user_id': info.context.user.pk})
        validator: CategoryValidator = CategoryValidator(data)
        if validator.validate():
            position: int = Category.objects.aggregate(Max('position'))['position__max']
            position = position + 1 if position is not None else 0
            return AddCategoryMutation(category=Category.objects.create(position=position, **data))
        else:
            return AddCategoryMutation(success=False, errors=ErrorFieldType.from_validator(validator.get_message()))


class ChangeCategoryMutation(BaseMutation):
    """Мутации для изменения категории"""
    class Input:
        category_id = graphene.ID(required=True, description='Идентификатор мутации')
        text = graphene.String(required=True, description='Название категории')

    category = graphene.Field(CategoryType, description='Добавленная котегория')

    @staticmethod
    @permission_classes([IsAuthenticated, ChangeCategory])
    def mutate_and_get_payload(root, info: ResolveInfo, category_id: str, text: str, *args, **kwargs):
        pk: int = from_global_id(category_id)[1]
        category: Category = get_object_or_404(Category, pk=pk)
        info.context.check_object_permissions(info.context, category)
        validator: CategoryValidator = CategoryValidator({'text': text})
        if not validator.validate():
            return ChangeCategoryMutation(success=False, errors=ErrorFieldType.from_validator(validator.get_message()))
        category.text = text
        category.save(update_fields=('text',))
        return ChangeCategoryMutation(category=category)


class ChangeCategoryAvatarMutation(BaseMutation):
    """Мутация для изменения аватара категории"""
    class Input:
        category_id = graphene.ID(required=True, description='Идентификатор мутации')
        avatar = Upload(description='Аватар')

    category = graphene.Field(CategoryType, description='Добавленная котегория')

    @staticmethod
    @permission_classes([IsAuthenticated, ChangeCategory])
    def mutate_and_get_payload(root, info: ResolveInfo, category_id: str, avatar: InMemoryUploadedFile, *args, **kwargs):
        pk: int = from_global_id(category_id)[1]
        category: Category = get_object_or_404(Category, pk=pk)
        info.context.check_object_permissions(info.context, category)
        category.avatar = avatar
        category.save(update_fields=('avatar',))
        return ChangeCategoryAvatarMutation(category=category)


class ChangeCategoryPositionMutation(BaseMutation):
    """Мутация для изменения порядка следования вывода категорий"""
    class Input:
        categories_id = graphene.List(graphene.ID, required=True, description='Идентификаторы категорий')

    @staticmethod
    @permission_classes([IsAuthenticated, ChangeAbsoluteCategory])
    def mutate_and_get_payload(root, info: ResolveInfo, categories_id: List[str], *args, **kwargs):
        categories_id: List[str] = [from_global_id(category_id)[1] for category_id in categories_id]
        with transaction.atomic():
            for index, category_id in enumerate(categories_id):
                Category.objects.filter(pk=category_id).update(position=index)
        return ChangeCategoryPositionMutation()


class ChangeCategoryParentMutation(BaseMutation):
    """Мутация для изменения родителя"""
    class Input:
        category_id = graphene.ID(required=True, description='Идентификатор категории')
        parent_id = graphene.ID(description='Идентификатор родителя')

    @staticmethod
    @permission_classes([IsAuthenticated, ChangeAbsoluteCategory])
    def mutate_and_get_payload(root, info: ResolveInfo, category_id: str, parent_id: str or None, *args, **kwargs):
        if parent_id is not None:
            parent_id = from_global_id(parent_id)[1]
        category: Category = get_object_or_404(Category, pk=from_global_id(category_id)[1])
        category.parent = get_object_or_none(Category, pk=parent_id)
        category.save(update_fields=('parent',))
        return ChangeCategoryParentMutation()


class DeleteCategoryMutation(BaseMutation):
    """Мутация для удаления категории"""
    class Input:
        category_id = graphene.ID(required=True, description='Идентификатор мутации')

    @staticmethod
    @permission_classes([IsAuthenticated, DeleteCategory])
    def mutate_and_get_payload(root, info: ResolveInfo, category_id: str, *args, **kwargs):
        category: Category = get_object_or_404(Category, pk=from_global_id(category_id)[1])
        info.context.check_object_permissions(info.context, category)
        category.delete()
        return DeleteCategoryMutation()


class CategoryMutations(graphene.ObjectType):
    add_category = AddCategoryMutation.Field(required=True)
    change_category = ChangeCategoryMutation.Field(required=True)
    change_category_avatar = ChangeCategoryAvatarMutation.Field(required=True)
    change_category_position = ChangeCategoryPositionMutation.Field(required=True)
    change_category_parent = ChangeCategoryParentMutation.Field(required=True)
    delete_category = DeleteCategoryMutation.Field(required=True)
