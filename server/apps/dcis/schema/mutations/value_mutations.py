"""Модуль содержит мутации, относящиеся к значениям ячеек."""
from typing import Sequence
import graphene
from graphql import ResolveInfo
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from apps.dcis.permissions import ChangeValue
from apps.dcis.schema.types import CellType


class SetValueMutation(BaseMutation):
    """Мутация для изменения значения в ячейки."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        cell_id = graphene.Int(required=True, description='Идентификатор изменяемой ячейки')
        value = graphene.String(required=True, description='Значение ячейки')

    cells = graphene.List(graphene.NonNull(CellType), required=True, description='Ячейки')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangeValue,))
    def mutate_and_get_payload(
            root,
            info: ResolveInfo,
            document_id: str,
            cell_id: int,
            value: str
    ) -> Sequence[CellType]:
        return []

class ValueMutations(graphene.ObjectType):
    """Мутации, связанные с ячейками."""
    set_value = SetValueMutation.Field(required=True, description='Установление значения документа')
