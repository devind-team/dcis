from typing import Any

import graphene
from devind_dictionaries.schema import OrganizationType
from devind_helpers.decorators import permission_classes
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.utils import gid2int
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.schema import UserType
from apps.dcis.schema.types import CuratorGroupType
from apps.dcis.services.curator_services import (
    add_curator_group,
    add_organization_curator_group,
    add_users_curator_group,
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
                user=info.context.user,
                name=name,
                group_id=group_id,
            )
        )


class DeleteCuratorGroupMutation(BaseMutation):
    """Мутация удаления кураторской группы."""

    class Input:
        curator_group_id = graphene.ID(required=True, description='Идентификатор кураторской группы')

    id = graphene.ID(description='Идентификатор удаленной кураторской группы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, curator_group_id: str):
        delete_curator_group(user=info.context.user, curator_group_id=curator_group_id)
        return DeleteCuratorGroupMutation(id=curator_group_id)


class AddUsersCuratorGroup(BaseMutation):
    """Мутация на добавление пользователей в кураторскую группу."""

    class Input:
        curator_group_id = graphene.ID(required=True, description='Идентификатор кураторской группы')
        user_ids = graphene.List(
            graphene.NonNull(graphene.ID),
            required=True,
            description='Идентификаторы пользователей'
        )

    users = graphene.List(UserType, description='Добавленные пользователи')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, curator_group_id: str, user_ids: list[str | int]):
        return AddUsersCuratorGroup(
            users=add_users_curator_group(
                user=info.context.user,
                curator_group_id=curator_group_id,
                user_ids=[gid2int(user_id) for user_id in user_ids],
            )
        )


class DeleteUserCuratorGroup(BaseMutation):
    """Мутация на добавление пользователей в кураторскую группу."""

    class Input:
        curator_group_id = graphene.ID(required=True, description='Идентификатор кураторской группы')
        user_id = graphene.ID(required=True, description='Идентификатор пользователя')

    id = graphene.ID(description='Идентификатор пользователя')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, curator_group_id: str, user_id: str | int):
        delete_user_curator_group(
            user=info.context.user,
            curator_group_id=curator_group_id,
            user_id=gid2int(user_id),
        )
        return DeleteUserCuratorGroup(id=user_id)


class AddOrganizationsCuratorGroup(BaseMutation):
    """Мутация на добавление организации в кураторскую группу."""

    class Input:
        curator_group_id = graphene.ID(required=True, description='Идентификатор кураторской группы')
        organization_ids = graphene.List(
            graphene.NonNull(graphene.ID),
            required=True,
            description='Идентификатор организации'
        )

    organizations = graphene.List(OrganizationType, description='Идентификатор организации')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, curator_group_id: str, organization_ids: list[str | int]):
        return AddOrganizationsCuratorGroup(
            organizations=add_organization_curator_group(
                user=info.context.user,
                curator_group_id=curator_group_id,
                organization_ids=[gid2int(organization_id) for organization_id in organization_ids],
            )
        )


class DeleteOrganizationCuratorGroup(BaseMutation):
    """Мутация на добавление пользователей в кураторскую группу."""

    class Input:
        curator_group_id = graphene.ID(required=True, description='Идентификатор кураторской группы')
        organization_id = graphene.ID(required=True, description='Идентификатор организации')

    id = graphene.ID(description='Идентификатор организации')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, curator_group_id: str, organization_id: str):
        delete_organization_curator_group(
            user=info.context.user,
            curator_group_id=curator_group_id,
            organization_id=from_global_id(organization_id)[1]
        )
        return DeleteOrganizationCuratorGroup(id=organization_id)


class CuratorMutations(graphene.ObjectType):
    """Список мутаций кураторов."""

    add_curator_group = AddCuratorGroupMutation.Field(required=True)
    delete_curator_group = DeleteCuratorGroupMutation.Field(required=True)

    add_users_curator_group = AddUsersCuratorGroup.Field(required=True)
    delete_user_curator_group = DeleteUserCuratorGroup.Field(required=True)

    add_organizations_curator_group = AddOrganizationsCuratorGroup.Field(required=True)
    delete_organization_curator_group = DeleteOrganizationCuratorGroup.Field(required=True)
