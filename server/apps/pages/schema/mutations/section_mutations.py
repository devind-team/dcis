from typing import Type, Tuple, List

import graphene
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Max
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.pages.models import Category, Page, Section
from apps.pages.permissions import AddSection, ChangeSection, DeleteSection
from apps.pages.validators import SectionValidator
from devind_core.models import File
from devind_helpers.schema.types import ErrorFieldType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_none
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from ..types import SectionTextType, SectionGalleryType, SectionFilesType


# ---------- Добавление  ----------

class AddSectionMutation(BaseMutation):
    """Базовая мутация для добавления секций"""
    class Meta:
        abstract = True

    class Input:
        page_id = graphene.ID(required=True, description='Идентификатор страницы')

    @staticmethod
    def get_page(page_id: str, base_mutation: Type[BaseMutation]) -> Tuple[Page or None, BaseMutation or None]:
        page: Page or None = get_object_or_none(Page, pk=from_global_id(page_id)[1])
        return (page, False,) \
            if page is not None \
            else (
                None,
                base_mutation(
                    success=False,
                    errors=[ErrorFieldType('page_id', [f'Страница {page_id} не существует'])]
                ),
            )


class AddSectionTextMutation(AddSectionMutation):
    """Добавление секции"""
    class Input(AddSectionMutation.Input):
        text = graphene.String(required=True, description='Текст страницы')

    section = graphene.Field(SectionTextType, description='Текстовое поле')

    @staticmethod
    @permission_classes([IsAuthenticated, AddSection])
    def mutate_and_get_payload(root, info: ResolveInfo, page_id: str, *args, **kwargs):
        page, error = AddSectionMutation.get_page(page_id, AddSectionTextMutation)
        if error:
            return error
        info.context.check_object_permissions(info.context, page)
        data = Section.resolve_global({**kwargs, 'page_id': page_id, 'user_id': info.context.user.pk})
        validator: SectionValidator = SectionValidator(data)
        if validator.validate():
            position: int = Category.objects.aggregate(Max('position'))['position__max']
            position: int = position + 1 if position is not None else 0
            return AddSectionTextMutation(
                section=Section.objects.create(kind=Section.TEXT, position=position, payload={}, **data)
            )
        else:
            return AddSectionTextMutation(success=False, errors=ErrorFieldType.from_validator(validator.get_message()))


class AddSectionGalleryMutation(AddSectionMutation):
    """Добавление секции"""
    class Input(AddSectionMutation.Input):
        text = graphene.String(required=True, description='Текст страницы')
        images = graphene.List(graphene.NonNull(Upload), required=True, description='Загружаемые изображения')

    section = graphene.Field(SectionGalleryType, description='Поле с файлами')

    @staticmethod
    @permission_classes([IsAuthenticated, AddSection])
    def mutate_and_get_payload(root, info: ResolveInfo, page_id: str, images: List[InMemoryUploadedFile], *args, **kwargs):
        page, error = AddSectionMutation.get_page(page_id, AddSectionGalleryMutation)
        if error:
            return error
        info.context.check_object_permissions(info.context, page)
        data = Section.resolve_global({**kwargs, 'page_id': page_id, 'user_id': info.context.user.pk})
        validator: SectionValidator = SectionValidator(data)
        if validator.validate():
            position: int = Category.objects.aggregate(Max('position'))['position__max']
            position: int = position + 1 if position is not None else 0
            img_list = File.objects.bulk_create([File(name=str(image), src=image, user_id=info.context.user.pk) for image in images])
            return AddSectionGalleryMutation(
                section=Section.objects.create(kind=Section.GALLERY, position=position, payload={'images': [image.id for image in img_list]}, **data)
            )
        else:
            return AddSectionGalleryMutation(success=False, errors=ErrorFieldType.from_validator(validator.get_message()))

class AddSectionFilesMutation(AddSectionMutation):
    """Добавление секции"""

    class Input(AddSectionMutation.Input):
        text = graphene.String(required=True, description='Текст страницы')
        files = graphene.List(graphene.NonNull(Upload), required=True, description='Загружаемые изображения')

    section = graphene.Field(SectionFilesType, description='Поле с файлами')

    @staticmethod
    @permission_classes([IsAuthenticated, AddSection])
    def mutate_and_get_payload(root, info: ResolveInfo, page_id: str, files: list[InMemoryUploadedFile], *args,
                               **kwargs):
        page, error = AddSectionMutation.get_page(page_id, AddSectionFilesMutation)
        if error:
            return error
        info.context.check_object_permissions(info.context, page)
        data = Section.resolve_global({**kwargs, 'page_id': page_id, 'user_id': info.context.user.pk})
        validator: SectionValidator = SectionValidator(data)
        if validator.validate():
            position: int = Category.objects.aggregate(Max('position'))['position__max']
            position: int = position + 1 if position is not None else 0
            file_list = File.objects.bulk_create(
                [File(name=str(file), src=file, user_id=info.context.user.pk) for file in files])
            return AddSectionFilesMutation(
                section=Section.objects.create(kind=Section.FILES, position=position,
                                               payload={'files': [file.id for file in file_list]}, **data)
            )
        else:
            return AddSectionFilesMutation(success=False,
                                             errors=ErrorFieldType.from_validator(validator.get_message()))

# ---------- Изменение секции ----------

class ChangeSectionMutation(BaseMutation):
    """Базовая мутация для изменения секций"""

    class Meta:
        abstract = True

    class Input:
        section_id = graphene.ID(required=True, description='Идентификатор секции')

    @staticmethod
    def get_section(section_id: int, base_mutation: Type[BaseMutation]) -> Tuple[Section or None, BaseMutation or None]:
        section: Section or None = get_object_or_none(Section, pk=section_id)
        return (section, False,) \
            if section is not None \
            else (
            None,
            base_mutation(
                success=False,
                errors=[ErrorFieldType('section_id', [f'Секции {section_id} не существует'])]
            ),
        )


class ChangeSectionTextMutation(ChangeSectionMutation):
    """Изменение текста секции"""
    class Input(ChangeSectionMutation.Input):
        text = graphene.String(required=True, description='Текст мутации')

    section = graphene.Field(SectionTextType, description='Текстовая секция')

    @staticmethod
    @permission_classes([IsAuthenticated, ChangeSection])
    def mutate_and_get_payload(root, info: ResolveInfo, section_id: int, text: str, *args, **kwargs):
        section, error = ChangeSectionMutation.get_section(section_id, ChangeSectionTextMutation)
        if error:
            return error
        info.context.check_object_permissions(info.context, section)
        validator: SectionValidator = SectionValidator({'text': text})
        if validator.validate():
            section.text = text
            section.save(update_fields=('text',))
            return ChangeSectionTextMutation(section=section)
        else:
            return ChangeSectionTextMutation(
                success=False,
                errors=ErrorFieldType.from_validator(validator.get_message())
            )


class ChangeSectionGalleryMutation(ChangeSectionMutation):
    """Изменение текста секции"""
    class Input(ChangeSectionMutation.Input):
        text = graphene.String(required=True, description='Текст мутации')
        new_images = graphene.List(graphene.NonNull(Upload), required=False, description='Загружаемые изображения')
        old_images = graphene.List(graphene.NonNull(graphene.ID), required=True, description='Изображения')

    section = graphene.Field(SectionGalleryType, description='Секция галереи')

    @staticmethod
    @permission_classes([IsAuthenticated, ChangeSection])
    def mutate_and_get_payload(root, info: ResolveInfo, section_id: int, text: str, new_images: List[InMemoryUploadedFile], old_images: List[str], *args, **kwargs):
        section, error = ChangeSectionMutation.get_section(section_id, ChangeSectionGalleryMutation)
        if error:
            return error
        info.context.check_object_permissions(info.context, section)
        validator: SectionValidator = SectionValidator({'text': text})
        if validator.validate():
            payload = {'images': []}
            for img_id in old_images:
                payload['images'].append(from_global_id(img_id)[1])
            new_img_list = File.objects.bulk_create(
                [File(name=str(image), src=image, user_id=info.context.user.pk) for image in new_images])
            payload['images'] += [image.id for image in new_img_list]
            section.text = text
            section.payload = payload
            section.save(update_fields=('text', 'payload'))
            return ChangeSectionGalleryMutation(section=section)
        else:
            return ChangeSectionGalleryMutation(
                success=False,
                errors=ErrorFieldType.from_validator(validator.get_message())
            )


class ChangeSectionFilesMutation(ChangeSectionMutation):
    """Изменение текста секции"""
    class Input(ChangeSectionMutation.Input):
        text = graphene.String(required=True, description='Текст мутации')
        new_files = graphene.List(graphene.NonNull(Upload), required=False, description='Загружаемые изображения')
        old_files = graphene.List(graphene.NonNull(graphene.ID), required=True, description='Изображения')

    section = graphene.Field(SectionFilesType, description='Секция галереи')

    @staticmethod
    @permission_classes([IsAuthenticated, ChangeSection])
    def mutate_and_get_payload(root, info: ResolveInfo, section_id: int, text: str, new_files: list[InMemoryUploadedFile], old_files: list[str], *args, **kwargs):
        section, error = ChangeSectionMutation.get_section(section_id, ChangeSectionFilesMutation)
        if error:
            return error
        info.context.check_object_permissions(info.context, section)
        validator: SectionValidator = SectionValidator({'text': text})
        if validator.validate():
            payload = {'files': []}
            for file_id in old_files:
                payload['files'].append(from_global_id(file_id)[1])
            new_file_list = File.objects.bulk_create(
                [File(name=str(file), src=file, user_id=info.context.user.pk) for file in new_files])
            payload['files'] += [file.id for file in new_file_list]
            section.text = text
            section.payload = payload
            section.save(update_fields=('text', 'payload'))
            return ChangeSectionFilesMutation(section=section)
        else:
            return ChangeSectionFilesMutation(
                success=False,
                errors=ErrorFieldType.from_validator(validator.get_message())
            )

# ---------- Удаление секции ----------


class DeleteSectionMutation(BaseMutation):
    """Удаление секции"""
    class Input:
        section_id = graphene.ID(required=True, description='Идентификатор секции')

    @staticmethod
    @permission_classes([IsAuthenticated, DeleteSection])
    def mutate_and_get_payload(root, info: ResolveInfo, section_id: str, *args, **kwargs):
        section: Section = Section.objects.get(pk=section_id)
        info.context.check_object_permissions(info.context, section)
        section.delete()
        return DeleteSectionMutation()


class SectionMutations(graphene.ObjectType):
    add_section_text = AddSectionTextMutation.Field(required=True)
    add_section_gallery = AddSectionGalleryMutation.Field(required=True)
    add_section_files = AddSectionFilesMutation.Field(required=True)
    change_section_text = ChangeSectionTextMutation.Field(required=True)
    change_section_gallery = ChangeSectionGalleryMutation.Field(required=True)
    change_section_files = ChangeSectionFilesMutation.Field(required=True)
    delete_section = DeleteSectionMutation.Field(required=True)
