"""Мутации, связанные с атрибутами."""
from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.mutation_factories import DeleteMutation
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.utils import gid2int
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo

from apps.dcis.models import Attribute, Document, Period
from apps.dcis.permissions import can_change_period_attributes
from apps.dcis.schema.types import AttributeType, AttributeValueType, ValueType
from apps.dcis.services.attribute_services import (
    change_attribute,
    change_attribute_value,
    create_attribute,
    unload_attributes_in_file,
    upload_attributes_from_file,
)


class AddAttributeMutation(BaseMutation):
    """Мутация для создания атрибута в периоде."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        name = graphene.String(required=True, description='Наименование атрибута')
        placeholder = graphene.String(required=True, description='Подсказка')
        key = graphene.String(required=True, description='Ключ')
        kind = graphene.String(required=True, description='Тип атрибута')
        default = graphene.String(required=True, description='Значение по умолчанию')
        mutable = graphene.Boolean(description='Можно ли изменять')

    attribute = graphene.Field(AttributeType, description='Добавленный аттрибут')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        period_id: str,
        name: str,
        placeholder: str,
        key: str,
        kind: str,
        default: str,
        mutable: bool
    ):
        period = get_object_or_404(Period, pk=gid2int(period_id))
        return AddAttributeMutation(
            attribute=create_attribute(
                user=info.context.user,
                period=period,
                name=name,
                placeholder=placeholder,
                key=key,
                kind=kind,
                default=default,
                mutable=mutable
            )
        )


class ChangeAttributeMutation(BaseMutation):
    """Мутация для изменения периода."""

    class Input:
        attribute_id = graphene.ID(required=True, description='Идентификатор периода')
        name = graphene.String(required=True, description='Наименование атрибута')
        placeholder = graphene.String(required=True, description='Подсказка')
        key = graphene.String(required=True, description='Ключ')
        kind = graphene.String(required=True, description='Тип атрибута')
        default = graphene.String(required=True, description='Значение по умолчанию')
        mutable = graphene.Boolean(description='Можно ли изменять')

    attribute = graphene.Field(AttributeType, description='Добавленный аттрибут')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        attribute_id: int,
        name: str,
        placeholder: str,
        key: str,
        kind: str,
        default: str,
        mutable: bool
    ):
        attribute: Attribute = get_object_or_404(Attribute, pk=attribute_id)
        return AddAttributeMutation(
            attribute=change_attribute(
                user=info.context.user,
                attribute=attribute,
                name=name,
                placeholder=placeholder,
                key=key,
                kind=kind,
                default=default,
                mutable=mutable
            )
        )


class ChangeAttributeValueMutation(BaseMutation):
    """Мутация для установки или изменения формы."""

    class Input:
        value = graphene.String(description='Значение атрибута.')
        attribute_id = graphene.ID(required=True, description='Идентификатор атрибута')
        document_id = graphene.ID(required=True, description='Идентификатор документа')

    attribute_value = graphene.Field(AttributeValueType, description='Измененное или созданное значение')
    values = graphene.List(ValueType, description='Измененные значения листов')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        value: str,
        attribute_id: int,
        document_id: str,
        *args, **kwargs
    ) -> 'ChangeAttributeValueMutation':
        document: Document = get_object_or_404(Document, pk=gid2int(document_id))
        attribute: Attribute = get_object_or_404(Attribute, pk=gid2int(attribute_id))
        attribute_value, values = change_attribute_value(info.context.user, attribute, document, value)
        return ChangeAttributeValueMutation(attribute_value=attribute_value, values=values)


class UploadAttributesFromFileMutation(BaseMutation):
    """Загрузка атребутов периода через json файл."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        attributes_file = Upload(required=True, description='json файл агрегации ячеек')

    attributes = graphene.List(AttributeType, description='Новая агрегация')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        period_id: str,
        attributes_file: InMemoryUploadedFile
    ):
        period = get_object_or_404(Period, pk=gid2int(period_id))
        return UploadAttributesFromFileMutation(
            attributes=upload_attributes_from_file(info.context.user, period, attributes_file)
        )


class UnloadAttributesInFileMutation(BaseMutation):
    """Выгрузка атребутов периода в json файл."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')

    src = graphene.String(description='Ссылка на сгенерированный файл')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, period_id: str):
        period = get_object_or_404(Period, pk=gid2int(period_id))
        return UnloadAttributesInFileMutation(
            src=unload_attributes_in_file(
                user=info.context.user,
                get_host=info.context.get_host(),
                period=period
            )
        )


class AttributeMutations(graphene.ObjectType):
    """Мутации, связанные с атрибутами."""

    add_attribute = AddAttributeMutation.Field(required=True, description='Добавление атрибута')
    change_attribute = ChangeAttributeMutation.Field(required=True, description='Изменение атрибута')
    delete_attribute = DeleteMutation(
        model=Attribute,
        check_permissions=lambda context, attribute: can_change_period_attributes(context.user, attribute.period)
    ).Field(required=True, description='Удаление атрибута')
    upload_attributes_from_file = UploadAttributesFromFileMutation.Field(
        required=True,
        description='Загрузка атребутов через json файл'
    )
    unload_attributes_in_file = UnloadAttributesInFileMutation.Field(required=True)

    change_attribute_value = ChangeAttributeValueMutation.Field(required=True, description='Изменение значения')
