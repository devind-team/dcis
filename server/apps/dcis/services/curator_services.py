"""Модуль, отвечающий за работу с кураторами."""

from devind_dictionaries.models import Organization
from devind_helpers.orm_utils import get_object_or_404
from django.db.models import QuerySet

from apps.core.models import User
from apps.dcis.models import CuratorGroup, Division, Document, Period
from apps.dcis.permissions.curator_permissions import (
    can_add_curator_group,
    can_change_curator_group,
    can_delete_curator_group,
)


def get_curator_groups(user: User) -> QuerySet[CuratorGroup]:
    """Возвращает кураторские группы, в который состоит пользователь `user`."""
    return CuratorGroup.objects.filter(users=user)


def get_curator_organizations(user: User) -> QuerySet[Organization]:
    """Возвращает организации, для которых пользователь `user` является куратором."""
    return Organization.objects.filter(curatorgroup__in=get_curator_groups(user))


def is_period_curator(user: User, period: Period) -> bool:
    """Является ли пользователь `user` куратором для периода `period`"""
    if period.project.division_name == 'department':
        return False
    organization_ids = get_curator_organizations(user).values_list('id', flat=True)
    return Division.objects.filter(period=period, object_id__in=organization_ids).count() > 0


def is_document_curator(user: User, document: Document) -> bool:
    """Является ли пользователь `user` куратором для документа `document`."""
    if document.period.project.division_name == 'department':
        return False
    organization_ids = get_curator_organizations(user).values_list('id', flat=True)
    return document.period.multiple and document.object_id in organization_ids or (
        not document.period.multiple and
        Division.objects.filter(period=document.period, object_id__in=organization_ids).count() > 0
    )


def get_curator_group_new_users(curator_group_id: str | int) -> QuerySet[User]:
    """Получение новых пользователей для кураторской группы."""
    return User.objects.exclude(curatorgroup__id=curator_group_id)


def get_curator_group_new_organizations() -> QuerySet[Organization]:
    """Получение новых организаций для кураторской группы."""
    return Organization.objects.exclude(curatorgroup__in=CuratorGroup.objects.all().values_list('id', flat=True))


def add_curator_group(user: User, name: str, group_id: str | int) -> CuratorGroup:
    """Добавление кураторской группы."""
    can_add_curator_group(user)
    return CuratorGroup.objects.create(name=name, group_id=group_id)


def delete_curator_group(user: User, curator_group_id: str | int) -> None:
    """Удаление кураторской группы."""
    can_delete_curator_group(user)
    curator_group: CuratorGroup = get_object_or_404(CuratorGroup, pk=curator_group_id)
    curator_group.delete()


def add_users_curator_group(user: User, curator_group_id: str | int, user_ids: list[str | int]) -> QuerySet[User]:
    """Добавление пользователей в кураторскую группу."""
    can_change_curator_group(user)
    curator_group: CuratorGroup = get_object_or_404(CuratorGroup, pk=curator_group_id)
    users = User.objects.filter(id__in=user_ids)
    for user in users:
        curator_group.users.add(user)
    return users


def delete_user_curator_group(user: User, curator_group_id: str | int, user_id: str | int) -> None:
    """Добавление пользователя в кураторскую группу."""
    can_change_curator_group(user)
    curator_group: CuratorGroup = get_object_or_404(CuratorGroup, pk=curator_group_id)
    curator_group.users.remove(user_id)


def add_organization_curator_group(
    user: User,
    curator_group_id: str | int,
    organization_ids: list[str | int]
) -> QuerySet[Organization]:
    """Добавление пользователя в кураторскую группу."""
    can_change_curator_group(user)
    curator_group: CuratorGroup = get_object_or_404(CuratorGroup, pk=curator_group_id)
    organizations = Organization.objects.filter(id__in=organization_ids)
    for organization in organizations:
        curator_group.organization.add(organization)
    return organizations


def delete_organization_curator_group(user: User, curator_group_id: str | int, organization_id: str | int) -> None:
    """Добавление пользователя в кураторскую группу."""
    can_change_curator_group(user)
    curator_group: CuratorGroup = get_object_or_404(CuratorGroup, pk=curator_group_id)
    curator_group.organization.remove(organization_id)
