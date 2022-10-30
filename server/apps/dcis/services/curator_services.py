"""Модуль, отвечающий за работу с кураторами."""
from devind_dictionaries.models import Organization
from django.db.models import QuerySet

from apps.core.models import User
from apps.dcis.models import CuratorGroup, Division, Document, Period


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
