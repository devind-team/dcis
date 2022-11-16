"""Тесты модуля, отвечающего за работу с периодами."""

from datetime import date, timedelta
from os.path import join
from shutil import rmtree
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department, Organization
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import (
    CuratorGroup,
    Division,
    Period,
    PeriodGroup,
    PeriodPrivilege,
    Privilege,
    Project,
)
from apps.dcis.permissions import (
    can_add_period,
    can_change_period_divisions,
    can_change_period_groups,
    can_change_period_settings,
    can_change_period_users,
    can_delete_period,
)
from apps.dcis.services.period_services import (
    add_divisions_period,
    add_period_group,
    change_period_group_privileges,
    change_settings_period,
    change_user_period_groups,
    change_user_period_privileges,
    copy_period_groups,
    create_period,
    delete_divisions_period,
    delete_period,
    delete_period_groups,
    get_user_curator_periods,
    get_user_divisions_periods,
    get_user_participant_periods,
    get_user_periods,
    get_user_privileges_periods,
)
from apps.dcis.tests.tests_helpers import create_in_memory_file
from devind.settings import BASE_DIR


class GetUserPeriodsTestCase(TestCase):
    """Тестирование получения периодов пользователя."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.organization_content_type = ContentType.objects.get_for_model(Organization)

        self.user = User.objects.create(username='user', email='user@gmain.com')
        self.extra_user = User.objects.create(username='extra_user', email='extra_user@gmail.com')

        self.user_is_creator_project = Project.objects.create(
            user=self.user,
            content_type=self.organization_content_type
        )
        self.user_project_periods = [Period.objects.create(project=self.user_is_creator_project) for _ in range(3)]

        self.user_is_not_creator_project = Project.objects.create(content_type=self.organization_content_type)
        self.user_periods = [Period.objects.create(
            user=self.user, project=self.user_is_not_creator_project
        ) for _ in range(3)]
        self.user_group_periods = [Period.objects.create(project=self.user_is_not_creator_project) for _ in range(3)]
        self.user_groups: list[PeriodGroup] = []
        for period in self.user_group_periods:
            self.user_groups.append(PeriodGroup.objects.create(period=period))
            self.user_groups[-1].users.add(self.user)

        self.curator_department_project = Project.objects.create(content_type=self.department_content_type)
        self.curator_department_periods = self._create_curator_periods(self.curator_department_project)
        self.curator_organization_periods = self._create_curator_periods(self.user_is_not_creator_project)

        self.privilege_period = Period.objects.create(project=self.user_is_not_creator_project)
        self.privilege = Privilege.objects.create()
        self.period_privilege = PeriodPrivilege.objects.create(
            period=self.privilege_period,
            user=self.user,
            privilege=self.privilege,
        )

        self.organization = Organization.objects.create(attributes='', user=self.user)
        self.organization_period = Period.objects.create(project=self.user_is_not_creator_project)
        self.organization_division = Division.objects.create(
            period=self.organization_period,
            object_id=self.organization.id,
        )

        self.extra_project = Project.objects.create(content_type=self.department_content_type)
        self.extra_period = Period.objects.create(project=self.extra_project)

    def test_get_user_participant_periods_user_is_project_creator(self) -> None:
        """Тестирование функции `get_user_participant_periods`, если пользователь является создателем проекта."""
        self.assertSetEqual(
            {*self.user_project_periods},
            set(get_user_participant_periods(self.user, self.user_is_creator_project.id)),
        )

    def test_get_user_participant_periods_user_is_not_project_creator(self) -> None:
        """Тестирование функции `get_user_participant_periods`, если пользователь не является создателем проекта."""
        self.assertSetEqual(
            {*self.user_periods, *self.user_group_periods},
            set(get_user_participant_periods(self.user, self.user_is_not_creator_project.id)),
        )

    def test_get_user_curator_periods_department_project(self) -> None:
        """Тестирование функции `get_user_curator_periods` для проекта с департаментами в качестве дивизионов."""
        self.assertQuerysetEqual(
            Period.objects.none(),
            get_user_curator_periods(self.user, self.curator_department_project.id),
        )

    def test_get_user_curator_periods_organization_project(self) -> None:
        """Тестирование функции `get_user_curator_periods` для проекта с организациями в качестве дивизионов."""
        self.assertEqual(
            {*self.curator_organization_periods},
            set(get_user_curator_periods(self.user, self.user_is_not_creator_project.id)),
        )

    def test_user_privileges_periods(self) -> None:
        """Тестирование функции `get_user_privileges_periods`."""
        self.assertSetEqual(
            {self.privilege_period},
            set(get_user_privileges_periods(self.user, self.user_is_not_creator_project.id))
        )

    def test_get_user_divisions_periods_without_periods(self) -> None:
        """Тестирование функции `get_user_divisions_periods` для пользователя, у которого нет периодов."""
        self.assertQuerysetEqual(
            Period.objects.none(),
            get_user_divisions_periods(self.extra_user, self.user_is_not_creator_project.id)
        )

    def test_get_user_divisions_periods_with_periods(self) -> None:
        """Тестирование функции `get_user_divisions_periods` для пользователя, у которого есть периоды."""
        self.assertSetEqual(
            {self.organization_period},
            set(get_user_divisions_periods(self.user, self.user_is_not_creator_project.id))
        )

    def test_user_periods_with_perm(self) -> None:
        """Тестирование функции `get_user_periods` при наличии у пользователя разрешения `dcis.view_period`."""
        with patch.object(self.user, 'has_perm', new=Mock(return_value=True)) as mock:
            periods = get_user_periods(self.user, self.extra_project)
            mock.assert_called_once_with('dcis.view_period')
            self.assertQuerysetEqual(self.extra_project.period_set.all(), periods)

    def test_user_periods_without_perm(self) -> None:
        """Тестирование функции `get_user_periods` при отсутствии у пользователя разрешения `dcis.view_period`."""
        self.assertSetEqual(
            {
                *self.user_periods,
                *self.user_group_periods,
                *self.curator_organization_periods,
                self.privilege_period,
                self.organization_period
            },
            set(get_user_periods(self.user, self.user_is_not_creator_project.id)),
        )

    def _create_curator_periods(self, project: Project) -> list[Period]:
        """Создание периодов для проекта c кураторской группой."""
        periods: list[Period] = []
        for _ in range(3):
            organization = Organization.objects.create(attributes='')
            period = Period.objects.create(project=project)
            period.division_set.create(object_id=organization.id)
            curator_group = CuratorGroup.objects.create()
            curator_group.users.add(self.user)
            curator_group.organization.add(organization)
            periods.append(period)
        return periods


class PeriodTestCase(TestCase):
    """Тестирование периода."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.department_content_type = ContentType.objects.get_for_model(Department)

        self.user = User.objects.create(username='user', email='user@gmain.com')
        self.super_user = User.objects.create(username='super_user', email='super_user@gmain.com', is_superuser=True)

        self.user_project = Project.objects.create(user=self.super_user, content_type=self.department_content_type)
        self.user_periods = [
            Period.objects.create(user=self.super_user, project=self.user_project, name=f'User period {number}') for
            number in range(3)
        ]
        self.user_period_groups: list[PeriodGroup] = []
        for period in self.user_periods:
            self.user_period_groups.append(PeriodGroup.objects.create(period=period, name=f'Group {period.name}'))
            self.user_period_groups[-1].users.add(self.super_user)
        self.user_period_group_id: list[str | int] = []
        self.user_period_group_id.append(self.user_period_groups[0].id)

        self.period_group_privileges: list[Privilege] = [
            Privilege.objects.create(name=f'Privilege {number + 1}', key=f'privilege_{number + 1}') for number in
            range(3)
        ]
        self.period_group_privileges_ids: list[str | int] = []
        for period_group_privilege_id in self.period_group_privileges:
            self.period_group_privileges_ids.append(period_group_privilege_id.id)

        self.departments = [
            Department.objects.create(user=self.super_user, name=f'Departament {number}') for number in range(3)
        ]
        self.departament_period = Period.objects.create(
            name='Departament period',
            user=self.super_user,
            project=self.user_project,
        )
        self.departament_period_groups = [PeriodGroup.objects.create(
            period=self.departament_period,
            name=f'Group departament {number + 1}'
        ) for number in range(3)]
        self.departament_period_group_ids: list[str | int] = []
        for period_group in self.departament_period_groups:
            self.departament_period_group_ids.append(period_group.id)
        self.departament_period_groups[0].privileges.set(self.period_group_privileges)
        self.departament_period_users_privileges = [
            Privilege.objects.create(name=f'Privileges user {number}', key=f'privileges_user_{number}') for number in
            range(3)
        ]
        self.departament_period_users_privileges_ids: list[str | int] = []
        for departament_period_users_privilege_id in self.departament_period_users_privileges:
            self.departament_period_users_privileges_ids.append(departament_period_users_privilege_id.id)
        self.department_divisions = [
            Division.objects.create(period=self.departament_period, object_id=departament.id)
            for departament in self.departments
        ]
        self.divisions_ids: list[str | int] = []
        for division_id in self.department_divisions:
            self.divisions_ids.append(division_id.object_id)

    def test_create_period(self) -> None:
        """Тестирование функции `get_create_period`."""
        with patch.object(self.user_project, 'user_id', new=None), patch.object(
            self.super_user,
            'has_perm',
            new=lambda perm: perm not in ('dcis.add_period', 'dcis.add_project')
        ):
            self.assertRaises(PermissionDenied, can_add_period, self.super_user, self.user_project)
        self.assertEqual(
            create_period(
                user=self.super_user,
                name='Test period',
                project=self.user_project,
                multiple=True,
                versioning=True,
                readonly_fill_color=False,
                xlsx_file=create_in_memory_file('test_create_period.xlsx'),
                limitations_file=None,
            ),
            Period.objects.get(name='Test period'),
            'Create period'
        )

    def test_add_divisions_period(self) -> None:
        """Тестирование функции `add_divisions_period`."""
        self._check_can_change_period(period=self.user_periods[0], permission=can_change_period_divisions)
        add_divisions_period(user=self.super_user, period_id=self.user_periods[0].id, division_ids=self.divisions_ids)

    def _check_can_change_period(self, period: Period, permission) -> None:
        """Тестирование permissions.

        `can_change_period_divisions`,
        `can_change_period_groups`,
        `can_change_period_users`,
        `can_change_period_settings`
        """
        with patch.object(period.project, 'user_id', new=None), patch.object(
            period,
            'user_id',
            new=None
        ), patch.object(
            self.super_user,
            'has_perm',
            new=lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, permission, self.super_user, period)

    def test_delete_divisions_period(self) -> None:
        """Тестирование функции `delete_divisions_period`."""
        self._check_can_change_period(period=self.departament_period, permission=can_change_period_divisions)
        self.assertEqual(
            delete_divisions_period(
                user=self.super_user,
                period_id=self.departament_period.id,
                division_id=self.divisions_ids[0]
            ),
            None,
            'Delete divisions'
        )

    def test_add_period_group(self) -> None:
        """Тестирование функции `add_period_group`."""
        self._check_can_change_period(period=self.departament_period, permission=can_change_period_groups)
        self.assertEqual(
            add_period_group(user=self.super_user, name='Group departament', period_id=self.departament_period.id),
            PeriodGroup.objects.get(name='Group departament'),
            'Create period group'
        )

    def test_copy_period_groups(self) -> None:
        """Тестирование функции `copy_period_groups`."""
        self._check_can_change_period(period=self.departament_period, permission=can_change_period_groups)
        self.copy_group = copy_period_groups(
            user=self.super_user,
            period_id=self.departament_period.id,
            period_group_ids=self.user_period_group_id,
            selected_period_id=self.user_periods[0].id
        )
        verify_groups = PeriodGroup.objects.filter(period_id=self.departament_period.id)
        for (copy, verify) in zip(self.copy_group, verify_groups):
            self.assertEqual(first=copy.name, second=verify.name, msg='Copy group')

    def test_change_period_group_privileges(self) -> None:
        """Тестирование функции `change_period_group_privileges`."""
        self._check_can_change_period(period=self.departament_period, permission=can_change_period_groups)
        self.assertEqual(
            first=change_period_group_privileges(
                user=self.super_user,
                period_group_id=self.departament_period_groups[0].id,
                privileges_ids=self.period_group_privileges_ids[: -1]
            ),
            second=list(
                self.departament_period_groups[0].privileges.filter(periodgroup=self.departament_period_groups[0])
            ),
            msg='Change period group privileges'
        )

    def test_change_user_period_groups(self) -> None:
        """Тестирование функции `change_user_period_groups`."""
        self._check_can_change_period(period=self.departament_period, permission=can_change_period_users)
        change_user_period_groups(user=self.super_user, period_group_ids=self.departament_period_group_ids)

    def test_change_user_period_privileges(self) -> None:
        """Тестирование функции `change_user_period_privileges`."""
        self._check_can_change_period(period=self.departament_period, permission=can_change_period_users)
        change_user_period_privileges(
            user=self.super_user,
            user_id=self.super_user.id,
            period_id=self.departament_period.id,
            privileges_ids=self.departament_period_users_privileges_ids
        )

    def test_change_settings_period(self) -> None:
        """Тестирование функции `change_settings_period`."""
        self._check_can_change_period(period=self.departament_period, permission=can_change_period_settings)
        self.assertEqual(
            change_settings_period(
                user=self.super_user,
                period=self.departament_period,
                name='Departament',
                status='В планах',
                multiple=True,
                versioning=True,
                privately=False,
                start=date.today(),
                expiration=date.today() + timedelta(days=7)
            ),
            Period.objects.get(name='Departament'),
            'Change period'
        )

    def test_delete_period_groups(self) -> None:
        """Тестирование функции `delete_period_groups`."""
        self._check_can_change_period(period=self.departament_period, permission=can_change_period_groups)
        self.assertEqual(
            delete_period_groups(user=self.super_user, period_group=self.departament_period_groups[0]),
            None,
            'Delete period_groups'
        )

    def test_delete_period(self) -> None:
        """Тестирование функции `delete_period`."""
        with patch.object(self.user_project, 'user_id', new=None), patch.object(
            self.departament_period,
            'user_id',
            new=None
        ), patch.object(
            self.super_user,
            'has_perm',
            new=lambda perm: perm not in ('dcis.delete_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, can_delete_period, self.super_user, self.departament_period)
        self.assertEqual(
            delete_period(user=self.super_user, period=self.departament_period),
            None,
            'Delete period'
        )

    def tearDown(self) -> None:
        """Очистка данных тестирования."""
        rmtree(join(BASE_DIR.parent, 'storage'), ignore_errors=True)
