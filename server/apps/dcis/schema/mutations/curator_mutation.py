from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from graphql import ResolveInfo

from apps.dcis.schema.types import CuratorGroupType
from apps.dcis.services.curator_services import (
    add_curator_group,
    add_organization_curator_group,
    add_user_curator_group,
    delete_curator_group,
    delete_organization_curator_group,
    delete_user_curator_group,
)


class AddCuratorGroupMutation(BaseMutation):
    """Мутация на добавление кураторской группы."""

    class Input:
        name = graphene.String(required=True, description='Название группы периода')
        group_id = graphene.ID(description='Идентификатор группы привилегий')

    curator_group = graphene.Field(CuratorGroupType, description='Добавленная кураторская группа')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, name: str, group_id: str):
        return AddCuratorGroupMutation(
            curator_group=add_curator_group(
                name=name,
                group_id=group_id,
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
        delete_curator_group(curator_group_id=curator_group_id)
        return DeleteCuratorGroupMutation(delete_id=curator_group_id)


class AddUserCuratorGroup(BaseMutation):
    """Мутация на добавление пользователей в кураторскую группу."""

    class Input:
        curator_group_id = graphene.ID(required=True, description='Идентификатор кураторской группы')
        user_id = graphene.ID(required=True, description='Идентификатор пользователя')

    add_user_id = graphene.ID(required=True, description='Идентификатор пользователя')

    @staticmethod
    # @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, curator_group_id: str | int, user_id: str | int):
        return AddUserCuratorGroup(
            add_user_id=add_user_curator_group(
                curator_group_id=curator_group_id,
                user_id=user_id
            )
        )


class DeleteUserCuratorGroup(BaseMutation):
    """Мутация на добавление пользователей в кураторскую группу."""

    class Input:
        curator_group_id = graphene.ID(required=True, description='Идентификатор кураторской группы')
        user_id = graphene.ID(required=True, description='Идентификатор пользователя')

    delete_id = graphene.ID(required=True, description='Идентификатор пользователя')

    @staticmethod
    # @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, curator_group_id: str | int, user_id: str | int):
        delete_user_curator_group(curator_group_id=curator_group_id, user_id=user_id)
        return AddUserCuratorGroup(delete_id=user_id)


class AddOrganizationCuratorGroup(BaseMutation):
    """Мутация на добавление организации в кураторскую группу."""

    class Input:
        curator_group_id = graphene.ID(required=True, description='Идентификатор кураторской группы')
        organization_id = graphene.ID(required=True, description='Идентификатор организации')

    add_organization_id = graphene.ID(required=True, description='Идентификатор организации')

    @staticmethod
    # @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, curator_group_id: str | int, organization_id: str | int):
        return AddOrganizationCuratorGroup(
            add_user_id=add_organization_curator_group(
                curator_group_id=curator_group_id,
                organization_id=organization_id
            )
        )


class DeleteUOrganizationCuratorGroup(BaseMutation):
    """Мутация на добавление пользователей в кураторскую группу."""

    class Input:
        curator_group_id = graphene.ID(required=True, description='Идентификатор кураторской группы')
        organization_id = graphene.ID(required=True, description='Идентификатор организации')

    delete_id = graphene.ID(required=True, description='Идентификатор организации')

    @staticmethod
    # @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, curator_group_id: str | int, organization_id: str | int):
        delete_organization_curator_group(curator_group_id=curator_group_id, organization_id=organization_id)
        return AddUserCuratorGroup(delete_id=organization_id)


class CuratorMutations(graphene.ObjectType):
    """Список мутаций кураторов."""

    add_curator_group = AddCuratorGroupMutation.Field(required=True)
    delete_curator_group = DeleteCuratorGroupMutation.Field(required=True)

    add_user_curator_group = AddUserCuratorGroup.Field(required=True)
    delete_user_curator_group = DeleteUserCuratorGroup.Field(required=True)

    add_organization_curator_group = AddOrganizationCuratorGroup.Field(required=True)
    delete_organization_curator_group = DeleteUOrganizationCuratorGroup.Field(required=True)
