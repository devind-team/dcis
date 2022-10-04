"""Мутации, связанные с атрибутами."""
from typing import Any

import graphene
from django.core.exceptions import PermissionDenied
from devind_helpers.utils import gid2int
from devind_helpers.schema.types import ErrorFieldType
from graphene_django.forms.mutation import DjangoModelFormMutation
from devind_helpers.schema.mutations import BaseMutation
from graphql import ResolveInfo
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.mutation_factories import DeleteMutation

from apps.dcis.services.attribute_service import change_attribute_value
from apps.dcis.permissions import can_change_value
from apps.dcis.permissions import can_change_period_sheet
from apps.dcis.models import Attribute, AttributeValue, Period, Document
from apps.dcis.forms import AddAttributeForm, ChangeAttributeForm
from apps.dcis.schema.types import AttributeValueType, ValueType
from apps.dcis.services.attribute_service import delete_attribute


class AddAttributeMutation(DjangoModelFormMutation):
    class Meta:
        form_class = AddAttributeForm
        return_field_name = 'attribute'

    @classmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(cls, root, info, **data):
        period = get_object_or_404(Period, pk=data.get('period'))
        can_change_period_sheet(info.context.user, period)
        return super().mutate_and_get_payload(root, info, **data)


class ChangeAttributeMutation(DjangoModelFormMutation):
    """Мутация для изменения периода."""

    class Meta:
        form_class = ChangeAttributeForm
        return_field_name = 'attribute'

    @classmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(cls, root, info, **data):
        attribute: Attribute = get_object_or_404(Attribute, pk=data.get('id'))
        can_change_period_sheet(info.context.user, attribute.period)
        return super().mutate_and_get_payload(root, info, **data)


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
        document_id: int | None = gid2int(document_id)
        document: Document = get_object_or_404(Document, pk=document_id)
        attribute: Attribute = get_object_or_404(Attribute, pk=attribute_id)
        attribute_value, value = change_attribute_value(info.context.user, attribute, document, value)
        return ChangeAttributeValueMutation(attribute_value=attribute_value, values=[])


class AttributeMutations(graphene.ObjectType):
    """Мутации, связанные с атрибутами."""

    add_attribute = AddAttributeMutation.Field(required=True, description='Добавление атрибута')
    change_attribute = ChangeAttributeMutation.Field(required=True, description='Изменение атрибута')
    delete_attribute = DeleteMutation(Attribute).Field(required=True, description='Удаление атрибута')

    change_attribute_value = ChangeAttributeValueMutation.Field(required=True, description='Изменение значения')
