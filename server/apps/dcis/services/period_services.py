"""Модуль, отвечающий за работу с периодами."""

from django.db.models import Q, QuerySet

from apps.core.models import User
from apps.dcis.models import Period, PeriodGroup, Privilege
from apps.dcis.services.divisions_services import get_user_division_ids


def get_user_participant_periods(user: User, project_id: int | str) -> QuerySet[Period]:
    """Получение периодов, в которых пользователь непосредственно участвует."""
    return Period.objects.filter(
        Q(project__user=user) | Q(user=user) | Q(periodgroup__users=user),
        project_id=project_id
    )


def get_user_privileges_periods(user: User, project_id: int | str) -> QuerySet[Period]:
    """Получение периодов, связанных с привилегиями пользователя."""
    return Period.objects.filter(periodprivilege__user=user, project_id=project_id)


def get_user_divisions_periods(user: User, project_id: int | str) -> QuerySet[Period]:
    """Получение периодов, связанных с дивизионами пользователя."""
    divisions = get_user_division_ids(user, project_id)
    periods = Period.objects.none()
    for division_name, division_values in divisions.items():
        periods |= Period.objects.filter(
            project__content_type__model=division_name,
            division__object_id__in=division_values,
            project_id=project_id
        )
    return periods


def get_user_periods(user: User, project_id: int | str) -> QuerySet[Period]:
    """Получение периодов пользователя для проекта.

    Пользователь видит период проекта:
      - пользователь обладает глобальной привилегией dcis.view_period
      - пользователь участвует в периоде
        (создал проект с периодом, или создал период, или состоит в группе периода)
      - пользователь имеет привилегию для периода
      - пользователь состоит в дивизионе, который участвует в периоде
    """
    if user.has_perm('dcis.view_period'):
        return Period.objects.filter(project_id=project_id)
    return get_user_participant_periods(
        user, project_id
    ) | get_user_divisions_periods(
        user, project_id
    ) | get_user_privileges_periods(
        user, project_id
    )


def get_user_period_privileges(user: User, period: Period) -> QuerySet[Privilege]:
    """Получение привилегий пользователя в периоде."""
    return Privilege.objects.filter(
        Q(periodgroup__period=period, periodgroup__users=user) |
        Q(periodprivilege__period=period, periodprivilege__user=user)
    )


def get_user_group_privileges(user: User, period_group: PeriodGroup) -> QuerySet[Privilege]:
    """Получение привилегий пользователя в группе периода."""
    return Privilege.objects.filter(
        Q(periodprivilege__user=user, periodprivilege__period_id=period_group.period_id) |
        Q(periodgroup=period_group, periodgroup__users=user)
    )
