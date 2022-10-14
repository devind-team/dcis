from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from graphql import ResolveInfo

from apps.dcis.schema.types import CuratorGroupType
from apps.dcis.services.curator_services import add_curator_group, delete_curator_group


class AddCuratorGroupMutation(BaseMutation):
    """Мутация на добавление кураторской группы."""

    class Input:
        name = graphene.String(required=True, description='Название группы периода')

    curator_group = graphene.Field(CuratorGroupType, description='Добавленная кураторская группа')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, name: str):
        return AddCuratorGroupMutation(
            curator_group=add_curator_group(
                name=name
            )
        )


class DeleteCuratorGroupMutation(BaseMutation):
    """Мутация удаления кураторской группы."""

    class Input:
        curator_group_id = graphene.ID(required=True, description='Идентификатор кураторской группы')

    delete_id = graphene.ID(required=True, description='Идентификатор удаленной кураторской группы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, curator_group_id: str | int):
        return DeleteCuratorGroupMutation(
            delete_id=delete_curator_group(
                curator_group_id=curator_group_id
            )
        )


class CuratorMutations(graphene.ObjectType):
    """Список мутаций кураторов."""

    add_curator_group = AddCuratorGroupMutation.Field(required=True)
    delete_curator_group = DeleteCuratorGroupMutation.Field(required=True)
