"""Модуль, отвечающий за работу с периодами."""

from django.db.models import Q, QuerySet

from apps.core.models import User
from apps.dcis.models import Period, Privilege
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


def get_period_users(period: Period | int | str) -> QuerySet[User]:
    """Получение пользователей, связанных с периодом."""
    period = Period.objects.get(pk=period) if type(period) in (int, str) else period
    divisions = period.project.division.objects.filter(
        pk__in=period.division_set.values_list('object_id', flat=True)
    )
    return User.objects.filter(
        Q(project__period__id=period.id) |
        Q(period__id=period.id) |
        Q(periodgroup__period__id=period.id) |
        Q(pk__in=[*divisions.values_list('user_id', flat=True), *divisions.values_list('users__id', flat=True)]) |
        Q(periodgroup__period__id=period.id) |
        Q(periodprivilege__period__id=period.id)
    ).distinct()


def get_user_period_privileges(user_id: int | str, period_id: int | str) -> QuerySet[Privilege]:
    """Получение отдельных привилегий пользователя в периоде."""
    return Privilege.objects.filter(periodprivilege__user__id=user_id, periodprivilege__period__id=period_id)
