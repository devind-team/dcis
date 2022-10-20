from devind_helpers.orm_utils import get_object_or_404

from apps.core.models import User
from apps.dcis.models import CuratorGroup
from apps.dcis.permissions.curator_permissions import can_add_curator_group


def add_curator_group(user: User, name: str, group_id: str | int) -> CuratorGroup:
    """Добавление кураторской группы."""
    can_add_curator_group(user)
    return CuratorGroup.objects.create(name=name, group_id=group_id)


def delete_curator_group(curator_group_id: str | int) -> None:
    """Удаление кураторской группы."""
    curator_group: CuratorGroup = get_object_or_404(CuratorGroup, pk=curator_group_id)
    curator_group.delete()


def add_user_curator_group(curator_group_id: str | int, user_id: str | int) -> str | int:
    """Добавление пользователя в кураторскую группу."""
    curator_group: CuratorGroup = get_object_or_404(CuratorGroup, pk=curator_group_id)
    curator_group.users.add(user_id)
    return user_id


def delete_user_curator_group(curator_group_id: str | int, user_id: str | int) -> None:
    """Добавление пользователя в кураторскую группу."""
    curator_group: CuratorGroup = get_object_or_404(CuratorGroup, pk=curator_group_id)
    curator_group.users.remove(user_id)


def add_organization_curator_group(curator_group_id: str | int, organization_id: str | int) -> str | int:
    """Добавление пользователя в кураторскую группу."""
    curator_group: CuratorGroup = get_object_or_404(CuratorGroup, pk=curator_group_id)
    curator_group.organization.add(organization_id)
    return organization_id


def delete_organization_curator_group(curator_group_id: str | int, organization_id: str | int) -> None:
    """Добавление пользователя в кураторскую группу."""
    curator_group: CuratorGroup = get_object_or_404(CuratorGroup, pk=curator_group_id)
    curator_group.organization.remove(organization_id)
