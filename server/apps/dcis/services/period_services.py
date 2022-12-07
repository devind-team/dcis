"""Модуль, отвечающий за работу с периодами."""

from datetime import date
from io import BytesIO
from typing import Type

from devind_dictionaries.models import Organization
from devind_helpers.import_from_file import ExcelReader
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.schema.types import ErrorFieldType
from devind_helpers.utils import convert_str_to_int
from django.core.exceptions import PermissionDenied
from django.core.files.base import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.db.models import Q, QuerySet

from apps.core.models import User
from apps.dcis.helpers.exceptions import is_raises
from apps.dcis.models import Attribute, Division, Period, PeriodGroup, PeriodPrivilege, Privilege, Project
from apps.dcis.permissions import (
    can_add_period,
    can_change_period_divisions,
    can_change_period_groups,
    can_change_period_settings,
    can_change_period_users,
    can_delete_period,
    can_view_period,
)
from apps.dcis.permissions.period_permissions import can_change_period_base
from apps.dcis.services.curator_services import get_curator_organizations, is_period_curator
from apps.dcis.services.divisions_services import get_divisions, get_user_division_ids
from apps.dcis.services.excel_extractor_services import ExcelExtractor
from apps.dcis.services.limitation_services import add_limitations_from_file


def get_user_participant_periods(user: User, project_id: int | str) -> QuerySet[Period]:
    """Получение периодов, в которых пользователь непосредственно участвует."""
    return Period.objects.filter(
        Q(project__user=user) | Q(user=user) | Q(periodgroup__users=user),
        project_id=project_id
    )


def get_user_curator_periods(user: User, project_id: int | str) -> QuerySet[Period]:
    """Получение периодов, для которых пользователь является куратором."""
    organization_ids = get_curator_organizations(user).values_list('id', flat=True)
    return Period.objects.filter(
        division__object_id__in=organization_ids,
        project__content_type__model='organization',
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
      - пользователь является куратором для периода
      - пользователь имеет привилегию для периода
      - пользователь состоит в дивизионе, который участвует в периоде
    """
    if user.has_perm('dcis.view_period'):
        return Period.objects.filter(project_id=project_id)
    return (
        get_user_participant_periods(user, project_id) |
        get_user_curator_periods(user, project_id) |
        get_user_divisions_periods(user, project_id) |
        get_user_privileges_periods(user, project_id)
    ).distinct()


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


def get_period_attributes(period: Period | int | str, parent: bool = True) -> QuerySet[Attribute]:
    """Получение атрибутов, связанных с периодом."""
    period = Period.objects.get(pk=period) if type(period) in (int, str) else period
    return (period.attribute_set.filter(parent__isnull=True) if parent else period.attribute_set).all()


def get_user_period_privileges(user_id: int | str, period_id: int | str) -> QuerySet[Privilege]:
    """Получение отдельных привилегий пользователя в периоде."""
    return Privilege.objects.filter(periodprivilege__user__id=user_id, periodprivilege__period__id=period_id)


def get_organizations_has_not_document(user: User, period: Period) -> QuerySet[Organization]:
    """Получение организаций, у которых не поданы документы в периоде."""
    organizations = Organization.objects.filter(
        id__in=period.division_set.exclude(
            object_id__in=period.document_set.values_list('object_id', flat=True)).values_list('object_id', flat=True)
    )
    if not is_raises(PermissionDenied, can_change_period_base, user, period):
        return organizations
    if is_period_curator(user, period):
        return organizations.filter(curatorgroup__id__in=user.curatorgroup_set.values_list('id', flat=True))
    raise PermissionDenied('Недостаточно прав для просмотра периода.')


@transaction.atomic
def create_period(
    user: User,
    name: str,
    project: Project,
    multiple: bool,
    versioning: bool,
    xlsx_file: File,
    limitations_file: File | None,
    readonly_fill_color: bool
) -> Period:
    """Создание периода."""
    can_add_period(user=user, project=project)
    period = Period.objects.create(
        name=name,
        user=user,
        project=project,
        multiple=multiple,
        versioning=versioning
    )
    fl = period.methodical_support.create(
        name=xlsx_file.name,
        src=xlsx_file,
        deleted=False,
        user=user
    )
    extractor = ExcelExtractor(fl.src.path, readonly_fill_color)
    extractor.save(period)
    if limitations_file is not None:
        add_limitations_from_file(period, limitations_file)
    return period


def add_divisions_period(user: User, period_id: str | int, division_ids: list[str | int]) -> list[dict[str, int | str]]:
    """Добавление дивизионов в период."""
    period = get_object_or_404(Period, pk=period_id)
    can_change_period_divisions(user=user, period=period)
    division_links = Division.objects.bulk_create(
        [
            Division(period=period, object_id=division_id) for division_id in division_ids
        ]
    )
    divisions = period.project.division.objects.filter(pk__in=[link.object_id for link in division_links])
    return get_divisions(divisions)


def add_divisions_from_file(
    user: User,
    period_id: str | int,
    file: InMemoryUploadedFile,
    field: str = 'idlistedu'
) -> tuple[list[dict[str, int | str]], list[int], list[ErrorFieldType] | None]:
    """Добавление дивизионов из файла формата csv/xlsx."""
    period = get_object_or_404(Period, pk=period_id)
    can_change_period_divisions(user, period)
    reader: ExcelReader = ExcelReader(BytesIO(file.read())) # noqa
    divisions_id: dict[int, int] = {}
    for item in reader.items:
        division_id: int | None = convert_str_to_int(item.get(field))
        if division_id:
            divisions_id[division_id] = 0
    if not divisions_id:
        return [], [], [
            ErrorFieldType('file', [f'Не найдено ни одной организации или отсутствует поле {field} в заголовке'])
        ],
    project: Project = period.project
    # 1. Подбираем найденные дивизионы
    divisions: dict[int, Type[project.division]] = project.division.objects \
        .filter(pk__in=divisions_id.keys()).in_bulk()
    # 2. Определяем переданные, но не найденные в базе данных
    for division_id in divisions:
        divisions_id[division_id] = 1
    missing_divisions = [division_id for division_id, freq in divisions_id.items() if freq == 0]
    # 3. Подбираем существующие дивизионы
    divisions_exist = period.division_set.values_list('object_id', flat=True)
    for division_exist in divisions_exist:
        divisions_id[division_exist] = 2
    # 4. Сохраняем в БД необходимые дивизионы
    income_divisions: dict[int, Type[project.division]] = {
        division_id: divisions[division_id]
        for division_id, freq in divisions_id.items() if freq == 1
    }
    with transaction.atomic():
        for income_division in income_divisions:
            period.division_set.create(object_id=income_division)
    return get_divisions(income_divisions.values()), missing_divisions, None,


def add_divisions_from_period(
    user: User,
    period_id: str | int,
    period_from_id: str | int
) -> tuple[list[dict[str, int | str]], list[ErrorFieldType] | None]:
    """Добавляем в период дивизионы из других периодов."""
    periods: dict[int, Period] = Period.objects \
        .filter(pk__in=[period_id, period_from_id]) \
        .select_related('project').in_bulk()
    if len(periods) != 2:
        return [], [ErrorFieldType('period_from_id', [f'Период не найден: {period_from_id}'])]
    period: Period = periods[period_id]
    period_from: Period = periods[period_from_id]
    can_change_period_divisions(user, period)
    can_change_period_divisions(user, period_from)
    if period.project.division != period_from.project.division:
        return [], [ErrorFieldType('period_from_id', ['Проекты имеют разные дивизионы'])]
    period_divisions_from: dict[int, int] = {
        division_id: 0 for division_id in period_from.division_set.values_list('object_id', flat=True)
    }
    period_divisions: list[int] = period.division_set.values_list('object_id', flat=True)
    for period_division in period_divisions:
        period_divisions_from[period_division] = 1
    Division = period.project.division # noqa
    divisions: dict[int, Type[Division]] = Division.objects \
        .filter(pk__in=[division_id for division_id, freq in period_divisions_from.items() if freq == 0]) \
        .in_bulk()
    with transaction.atomic():
        for division_id in divisions:
            period.division_set.create(object_id=division_id)
    return get_divisions(divisions.values()), None


def delete_divisions_period(user: User, period_id: str | int, division_id: str | int) -> None:
    """Удаление дивизиона из периода."""
    period = get_object_or_404(Period, pk=period_id)
    can_change_period_divisions(user=user, period=period)
    Division.objects.get(period_id=period_id, object_id=division_id).delete()


def add_period_group(user: User, name: str, period_id: str | int) -> PeriodGroup:
    """Добавление группы в период."""
    period = get_object_or_404(Period, pk=period_id)
    can_change_period_groups(user=user, period=period)
    return PeriodGroup.objects.create(
        name=name,
        period_id=period_id,
    )


def copy_period_groups(
    user: User,
    period_id: str | int,
    period_group_ids: list[str | int],
    selected_period_id: str | int
) -> list[PeriodGroup]:
    """Перенос групп из другого периода."""
    period = get_object_or_404(Period, pk=period_id)
    can_change_period_groups(user, period)
    selected_period = get_object_or_404(Period, pk=selected_period_id)
    can_view_period(user, selected_period)
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
    user: User,
    period_group_id: str | int,
    privileges_ids: list[str | int]
) -> list[Privilege]:
    """Изменение привилегий группы."""
    period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
    can_change_period_groups(user, period_group.period)
    privileges: list[Privilege] = []
    for privilege_id in privileges_ids:
        privilege = get_object_or_404(Privilege, pk=privilege_id)
        privileges.append(privilege)
    period_group.privileges.set(privileges)
    return privileges


def change_user_period_groups(permission_user: User, user: User, period_group_ids: list[str | int]) -> list[PeriodGroup]:
    """Изменение групп пользователя в периоде."""
    period_groups: list[PeriodGroup] = []
    for period_group_id in period_group_ids:
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        can_change_period_users(permission_user, period_group.period)
        period_groups.append(period_group)
    user.periodgroup_set.set(period_groups)
    return period_groups


def change_user_period_privileges(
    user: User,
    user_id: str | int,
    period_id: str | int,
    privileges_ids: list[str | int]
) -> list[Privilege]:
    """Изменение отдельных привилегий пользователя в периоде."""
    period = get_object_or_404(Period, pk=period_id)
    can_change_period_users(user, period)
    PeriodPrivilege.objects.filter(period_id=period_id, user_id=user_id).delete()
    privileges: list[Privilege] = []
    for privileges_id in privileges_ids:
        privilege = get_object_or_404(Privilege, pk=privileges_id)
        PeriodPrivilege.objects.create(period_id=period_id, user_id=user_id, privilege=privilege)
        privileges.append(privilege)
    return privileges


def change_settings_period(
    user: User,
    period: Period,
    name: str,
    status: str,
    multiple: bool,
    versioning: bool,
    privately: bool,
    start: date,
    expiration: date
) -> Period:
    """Изменение настроек периода."""
    can_change_period_settings(user, period)
    period.name = name
    period.status = status
    period.multiple = multiple
    period.versioning = versioning
    period.privately = privately
    period.start = start
    period.expiration = expiration
    period.save()
    return period


def delete_period(user: User, period: Period) -> None:
    """Удаление периода."""
    can_delete_period(user, period)
    period.delete()


def delete_period_groups(user: User, period_group: PeriodGroup) -> None:
    """Удаление группы периода."""
    can_change_period_groups(user, period_group.period)
    period_group.delete()
