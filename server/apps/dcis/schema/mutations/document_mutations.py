import graphene
from devind_helpers.schema.mutations import BaseMutation
from graphql import ResolveInfo

from apps.dcis.models import Value
from apps.dcis.schema.types import ValueType


class ChangeValue(BaseMutation):
    """Изменение значения."""

    class Input:
        value_id = graphene.ID(required=True, description='Идентификатор значения')
        value = graphene.String(required=True, description='Значение')

    value = graphene.Field(ValueType, description='Измененное значение')

    @staticmethod
    def mutate_and_get_payload(root: None, info: ResolveInfo, value_id: str, value: str):
        value_obj = Value.objects.get(pk=value_id)
        value_obj.value = value
        value_obj.save()
        return ChangeValue(value=value_obj)


class DocumentMutations(graphene.ObjectType):
    """Мутации, связанные с документами."""

    change_value = ChangeValue.Field(required=True)
