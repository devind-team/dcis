"""Тесты модуля, отвечающего за работу с периодами."""
from os.path import join
from shutil import rmtree
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from six import BytesIO

from apps.core.models import User
from apps.dcis.models import Division, Period, PeriodGroup, PeriodPrivilege, Privilege, Project
from apps.dcis.permissions import can_add_period, can_change_period_divisions, can_change_period_groups, can_view_period
from apps.dcis.services.period_services import (
    add_divisions_period,
    add_period_group,
    copy_period_groups,
    create_period,
    delete_divisions_period,
    get_user_divisions_periods,
    get_user_participant_periods,
    get_user_periods,
    get_user_privileges_periods,
)
from devind.settings import BASE_DIR


class GetUserPeriodsTestCase(TestCase):
    """Тестирование получения периодов пользователя."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.department_content_type = ContentType.objects.get_for_model(Department)

        self.user = User.objects.create(username='user', email='user@gmain.com')
        self.extra_user = User.objects.create(username='extra_user', email='extra_user@gmail.com')

        self.user_is_creator_project = Project.objects.create(user=self.user, content_type=self.department_content_type)
        self.user_project_periods = [Period.objects.create(project=self.user_is_creator_project) for _ in range(3)]

        self.user_is_not_creator_project = Project.objects.create(content_type=self.department_content_type)
        self.user_periods = [Period.objects.create(
            user=self.user, project=self.user_is_not_creator_project
        ) for _ in range(3)]
        self.user_group_periods = [Period.objects.create(project=self.user_is_not_creator_project) for _ in range(3)]
        self.user_groups: list[PeriodGroup] = []
        for period in self.user_group_periods:
            self.user_groups.append(PeriodGroup.objects.create(period=period))
            self.user_groups[-1].users.add(self.user)

        self.privilege_period = Period.objects.create(project=self.user_is_not_creator_project)
        self.privilege = Privilege.objects.create()
        self.period_privilege = PeriodPrivilege.objects.create(
            period=self.privilege_period,
            user=self.user,
            privilege=self.privilege,
        )

        self.department = Department.objects.create(user=self.user)
        self.department_period = Period.objects.create(project=self.user_is_not_creator_project)
        self.department_division = Division.objects.create(period=self.department_period, object_id=self.department.id)

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
            {self.department_period},
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
                self.privilege_period,
                self.department_period
            },
            set(get_user_periods(self.user, self.user_is_not_creator_project.id)),
        )


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
        self.user_periods = [
            Period.objects.create(project=self.user_project, name=f'Period {number + 1}') for number in range(3)
        ]
        self.user_groups: list[PeriodGroup] = []
        for period in self.user_periods:
            self.user_groups.append(PeriodGroup.objects.create(period=period, name=f'Group {period.name}'))
            self.user_groups[-1].users.add(self.super_user)

        self.user_groups_id: list[str | int] = []
        self.user_groups_id.append(self.user_groups[0].id)

        self.departaments = [
            Department.objects.create(user=self.super_user, name=f'Departament {number}') for number in range(3)
        ]
        self.department_period = Period.objects.create(
            user=self.super_user,
            project=self.user_project,
            name='Departament period'
        )
        self.department_divisions = [Division.objects.create(period=self.department_period, object_id=departament.id)
                                     for departament in self.departaments]

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
        with open(
            file=join(BASE_DIR, 'apps', 'dcis', 'tests', 'resources', 'test_create_period.xlsx'),
            mode='rb'
        ) as file:
            self.assertEqual(
                create_period(
                    user=self.super_user,
                    name='Test period',
                    project=self.user_project,
                    multiple=True,
                    file=self._create_inmemory_file(
                        file_name=file.name,
                        content=file.read(),
                        content_type=None
                    ),
                    readonly_fill_color=False
                ),
                Period.objects.get(name='Test period'),
                'Create period'
            )

    def _create_inmemory_file(
        self,
        file_name: str,
        content: bytes,
        content_type: None
    ) -> InMemoryUploadedFile:
        self.stream = BytesIO()
        self.stream.write(content)
        self.file = InMemoryUploadedFile(
            file=self.stream,
            field_name=None,
            name=file_name,
            content_type=content_type,
            size=self.stream.tell(),
            charset=None
        )
        self.file.seek(0)
        return self.file

    def test_add_divisions_period(self) -> None:
        """Тестирование функции `add_divisions_period`."""
        self._check_can_change_period(period=self.user_periods[0], permission=can_change_period_divisions)
        add_divisions_period(user=self.super_user, period_id=self.user_periods[0].id, division_ids=self.divisions_ids)

    def _check_can_change_period(self, period: Period, permission) -> None:
        """Тестирование permissions.

        `can_change_period_divisions`,
        `can_change_period_groups`
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
        self._check_can_change_period(period=self.department_period, permission=can_change_period_divisions)
        self.assertEqual(
            delete_divisions_period(
                user=self.super_user,
                period_id=self.department_period.id,
                division_id=self.divisions_ids[0]
            ),
            None,
            'Delete divisions'
        )

    def test_add_period_group(self) -> None:
        """Тестирование функции `add_period_group`."""
        self._check_can_change_period(period=self.department_period, permission=can_change_period_groups)
        self.assertEqual(
            add_period_group(user=self.super_user, name='Group departament', period_id=self.department_period.id),
            PeriodGroup.objects.get(name='Group departament'),
            'Create period group'
        )

    def test_copy_period_groups(self) -> None:
        """Тестирование функции `copy_period_groups`."""
        self._check_can_change_period(period=self.department_period, permission=can_change_period_groups)
        self.copy_group = copy_period_groups(
            user=self.super_user,
            period_id=self.department_period.id,
            period_group_ids=self.user_groups_id,
            selected_period_id=self.user_periods[0].id
        )
        self.verify_group: list[PeriodGroup] = []
        self.verify_group.append((PeriodGroup.objects.get(period_id=self.department_period.id)))
        for (copy, verify) in zip(self.copy_group, self.verify_group):
            self.assertEqual(first=copy.name, second=verify.name, msg='Copy group')

    def tearDown(self) -> None:
        """Очистка данных тестирования."""
        rmtree(join(BASE_DIR.parent, 'storage'), ignore_errors=True)
