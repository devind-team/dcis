"""Мутации, связанные с атрибутами."""
from typing import Any

import graphene
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql import ResolveInfo
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.mutation_factories import DeleteMutation

from apps.dcis.permissions import can_change_period_sheet
from apps.dcis.models import Attribute, Period
from apps.dcis.forms import AddAttributeForm, ChangeAttributeForm
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


class AttributeMutations(graphene.ObjectType):
    """Мутации, связанные с атрибутами."""

    add_attribute = AddAttributeMutation.Field(required=True)
    change_attribute = ChangeAttributeMutation.Field(required=True)
    delete_attribute = DeleteMutation(Attribute).Field(required=True)