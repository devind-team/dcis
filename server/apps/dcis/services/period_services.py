"""Модуль, отвечающий за работу с периодами."""

from datetime import date

from devind_core.models import File
from devind_helpers.orm_utils import get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q, QuerySet
from graphql import ResolveInfo

from apps.core.models import User
from apps.dcis.models import Division, Period, PeriodGroup, PeriodPrivilege, Privilege, Project
from apps.dcis.permissions import (
    can_add_period,
    can_change_period_divisions,
    can_change_period_groups,
    can_change_period_settings,
    can_change_period_users,
    can_delete_period,
    can_view_period
)
from apps.dcis.services.divisions_services import get_divisions, get_user_division_ids


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


def create_period(name: str, user: User, project: Project, multiple: bool) -> Period:
    """Создание периода."""
    can_add_period(user, project)
    return Period.objects.create(
            name=name,
            user=user,
            project=project,
            multiple=multiple
        )


def add_period_methodical_support(period: Period, file: InMemoryUploadedFile, user: User) -> File:
    """Добавление файлов в период."""
    return period.methodical_support.create(
            name=file.name,
            src=file,
            deleted=False,
            user=user
        )


def add_divisions_period(info: ResolveInfo, period_id: str | int, division_ids: list[str | int]) -> list[dict[str, int | str]]:
    """Добавление дивизионов в период."""
    period = get_object_or_404(Period, pk=period_id)
    can_change_period_divisions(info.context.user, period)
    division_links = Division.objects.bulk_create([
        Division(period=period, object_id=division_id) for division_id in division_ids
    ])
    divisions = period.project.division.objects.filter(pk__in=[link.object_id for link in division_links])
    return get_divisions(divisions)


def delete_divisions_period(info: ResolveInfo, period_id: str | int, division_id: str | int) -> None:
    """Удаление дивизиона из периода."""
    period = get_object_or_404(Period, pk=period_id)
    can_change_period_divisions(info.context.user, period)
    Division.objects.get(period_id=period_id, object_id=division_id).delete()


def copy_period_groups(
        info: ResolveInfo,
        period_id: str | int,
        period_group_ids: list[str | int],
        selected_period_id: str | int) -> list[PeriodGroup]:
    """Перенос групп из другого периода."""
    period = get_object_or_404(Period, pk=period_id)
    can_change_period_groups(info.context.user, period)
    selected_period = get_object_or_404(Period, pk=selected_period_id)
    can_view_period(info.context.user, selected_period)
    period_groups: list[PeriodGroup] = []
    for period_group_id in period_group_ids:
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        period_groups.append(period_group)
        new_group = PeriodGroup.objects.create(name=period_group.name, period=period)
        new_group.users.set(period_group.users.all())
        new_group.privileges.set(period_group.privileges.all())
        for user in period_group.users.all():
            for period_privilege in user.periodprivilege_set.filter(period=selected_period).all():
                PeriodPrivilege.objects.create(period=period, user=user, privilege=period_privilege.privilege)
    return period_groups


def change_period_group_privileges(
        info: ResolveInfo,
        period_group_id: str | int,
        privileges_ids: list[str | int]) -> list[Privilege]:
    """Изменение привилегий группы."""
    period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
    can_change_period_groups(info.context.user, period_group.period)
    privileges: list[Privilege] = []
    for privilege_id in privileges_ids:
        privilege = get_object_or_404(Privilege, pk=privilege_id)
        privileges.append(privilege)
    period_group.privileges.set(privileges)
    return privileges


def change_user_period_groups(info: ResolveInfo, period_group_ids: list[PeriodGroup]) -> list[PeriodGroup]:
    """Изменение групп пользователя в периоде."""
    period_groups: list[PeriodGroup] = []
    for period_group_id in period_group_ids:
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        can_change_period_users(info.context.user, period_group.period)
        period_groups.append(period_group)
    return period_groups


def change_user_period_privileges(
        info: ResolveInfo,
        user_id: str | int,
        period_id: str | int,
        privileges_ids: list[str | int]) -> list[Privilege]:
    """Изменение отдельных привилегий пользователя в периоде."""
    period = get_object_or_404(Period, pk=period_id)
    can_change_period_users(info.context.user, period)
    PeriodPrivilege.objects.filter(period_id=period_id, user_id=user_id).delete()
    privileges: list[Privilege] = []
    for privileges_id in privileges_ids:
        privilege = get_object_or_404(Privilege, pk=privileges_id)
        PeriodPrivilege.objects.create(period_id=period_id, user_id=user_id, privilege=privilege)
        privileges.append(privilege)
    return privileges


def add_period_group(info: ResolveInfo, name: str, period_id: str | int) -> PeriodGroup:
    """Добавление группы в период."""
    period = get_object_or_404(Period, pk=period_id)
    can_change_period_groups(info.context.user, period)
    return PeriodGroup.objects.create(
            name=name,
            period_id=period_id,
        )


def change_settings_period(
        info: ResolveInfo,
        period: Period,
        name: str,
        status: str,
        multiple: bool,
        privately: bool,
        start: date,
        expiration: date) -> Period:
    """Изменение настроек периода."""
    can_change_period_settings(info.context.user, period)
    period.name = name
    period.status = status
    period.multiple = multiple
    period.privately = privately
    period.start = start
    period.expiration = expiration
    period.save()
    return period


def delete_period(info: ResolveInfo, period: Period) -> None:
    """Удаление периода."""
    can_delete_period(info.context.user, period)
    period.delete()


def delete_period_groups(info: ResolveInfo, period_group: PeriodGroup) -> None:
    """Удаление группы периода."""
    can_change_period_groups(info.context.user, period_group.period)
    period_group.delete()

