"""Модуль, отвечающий за работу с привилегиями."""

from apps.dcis.models import PeriodGroup, PeriodPrivilege


def has_privilege(user_id: int | str, period_id: int | str, key: str) -> bool:
    """Обладает ли пользователь привилегией.

    Обладает ли пользователь с идентификатором user_id привилегией с ключом key
    для периода с идентификатором period_id или состоит в группе с наличием этой привилегии.
    """
    return has_individual_privilege(user_id, period_id, key) or has_group_privilege(user_id, period_id, key)


def has_individual_privilege(user_id: int | str, period_id: int | str, key: str) -> bool:
    """Обладает ли пользователь индивидуальной привилегией.

    Обладает ли пользователь с идентификатором user_id привилегией с ключом key
    для периода с идентификатором period_id.
    """
    return bool(PeriodPrivilege.objects.filter(user_id=user_id, period_id=period_id, privilege__key=key).first())


def has_group_privilege(user_id: int | str, period_id: int | str, key: str) -> bool:
    """Обладает ли пользователь групповой привилегией.

    Состоит ли пользователь с идентификатором user_id в группе, имеющей привилегию key
    для периода с идентификатором period_id.
    """
    return bool(PeriodGroup.objects.filter(period_id=period_id, users__id=user_id, privileges__key=key).first())
