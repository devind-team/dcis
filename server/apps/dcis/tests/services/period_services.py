"""Тесты модуля, отвечающего за работу с периодами."""

from datetime import date, timedelta
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department, Organization
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import (
    CuratorGroup,
    Division,
    Document, Period,
    PeriodGroup,
    PeriodPrivilege,
    Privilege,
    Project,
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
    get_organizations_has_not_document, get_user_curator_periods,
    get_user_divisions_periods,
    get_user_participant_periods,
    get_user_periods,
    get_user_privileges_periods,
)
from apps.dcis.tests.tests_helpers import create_in_memory_file


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
    """Тестирование основных действий с периодом."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.organization_content_type = ContentType.objects.get_for_model(Organization)

        self.project = Project.objects.create(user=self.superuser, content_type=self.organization_content_type)
        self.period = Period.objects.create(name='Period', user=self.superuser, project=self.project)

        self.change_period_settings_data = {
            'user': self.superuser,
            'name': 'Departament',
            'status': 'В планах',
            'multiple': True,
            'versioning': True,
            'privately': True,
            'start': date.today(),
            'expiration':date.today() + timedelta(days=7),
        }

    def test_create_period(self) -> None:
        """Тестирование функции `create_period`."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm not in ('dcis.add_period', 'dcis.add_project')
        ):
            self.assertRaises(PermissionDenied, self._create_period)
        actual_period = self._create_period()
        expected_period = Period.objects.get(name='Test period')
        self.assertEqual(expected_period, actual_period)

    def test_delete_period(self) -> None:
        """Тестирование функции `delete_period`."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm not in ('dcis.delete_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, self._delete_period)
        self.assertEqual(None, self._delete_period())
        self.assertQuerysetEqual(Period.objects.none(), Period.objects.filter(name='Period'))

    def test_change_settings_period(self) -> None:
        """Тестирование функции `change_settings_period`."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, self._change_period_settings)
        actual_period = self._change_period_settings()
        self.assertEqual(self.period, actual_period)
        for k, v in self.change_period_settings_data.items():
            self.assertEqual(v, getattr(actual_period, k))

    def _create_period(self) -> Period:
        """Вызов функции `create_period`."""
        return create_period(
            user=self.superuser,
            name='Test period',
            project=self.project,
            multiple=True,
            versioning=True,
            readonly_fill_color=False,
            xlsx_file=create_in_memory_file('test_create_period.xlsx'),
            limitations_file=None,
        )

    def _delete_period(self) -> None:
        """Вызов функции `delete_period`."""
        return delete_period(user=self.superuser, period=self.period)

    def _change_period_settings(self) -> Period:
        """Вызов функции `change_period_settings`."""
        return change_settings_period(
            period=self.period,
            **self.change_period_settings_data,
        )


class PeriodDivisionTestCase(TestCase):
    """Тестирование дивизионов периода."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.organization_content_type = ContentType.objects.get_for_model(Organization)

        self.project = Project.objects.create(user=self.superuser, content_type=self.organization_content_type)
        self.period = Period.objects.create(name='Period', user=self.superuser, project=self.project)

        self.organizations = [Organization.objects.create(name=f'Organization {i}', attributes='') for i in range(3)]
        self.organization_ids = [o.id for o in self.organizations]

        self.organization_to_delete = Organization.objects.create(name='Organization to delete', attributes='')
        self.period.division_set.create(object_id=self.organization_to_delete.id)

    def test_add_divisions_period(self) -> None:
        """Тестирование функции `add_divisions_period`."""
        with patch.object(
            self.superuser,
            'has_perm',
            lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, self._add_divisions_period)
        self.assertEqual(
            [{'id': o.id, 'name': o.name, 'model': 'organization'} for o in self.organizations],
            self._add_divisions_period()
        )

    def test_delete_divisions_period(self) -> None:
        """Тестирование функции `delete_divisions_period`."""
        with patch.object(
            self.superuser,
            'has_perm',
            lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, self._delete_divisions_period)
        self.assertEqual(None, self._delete_divisions_period())
        self.assertQuerysetEqual(
            Division.objects.none(),
            Division.objects.filter(object_id=self.organization_to_delete.id)
        )

    def _add_divisions_period(self) -> list[dict[str, int | str]]:
        """Вызов функции `add_divisions_period`."""
        return add_divisions_period(user=self.superuser, period_id=self.period.id, division_ids=self.organization_ids)

    def _delete_divisions_period(self) -> None:
        """Вызов функции `delete_divisions_period`."""
        return delete_divisions_period(
            user=self.superuser,
            period_id=self.period.id,
            division_id=self.organization_to_delete.id
        )


class PeriodGroupTestCase(TestCase):
    """Тестирование групп периода."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.organization_content_type = ContentType.objects.get_for_model(Organization)

        self.project = Project.objects.create(user=self.superuser, content_type=self.organization_content_type)
        self.period = Period.objects.create(name='Period', user=self.superuser, project=self.project)

        self.selected_period = Period.objects.create(name='Source period', user=self.superuser, project=self.project)
        self.selected_period_groups = [
            PeriodGroup.objects.create(name=f'Period group {i}', period=self.selected_period) for i in range(3)
        ]

        self.privileges_period = Period.objects.create(
            name='Privileges period',
            user=self.superuser,
            project=self.project
        )
        self.privileges_period_group = PeriodGroup.objects.create(
            name='Privileges period group',
            period=self.privileges_period
        )
        self.privileges = [
            Privilege.objects.create(name=f'Privilege {i + 1}', key=f'privilege_{i + 1}') for i in
            range(3)
        ]

        self.period_to_delete_groups = Period.objects.create(
            name='Period to delete groups',
            user=self.superuser,
            project=self.project
        )
        self.groups_to_delete = [
            PeriodGroup.objects.create(name=f'Group to delete {i}', period=self.period_to_delete_groups)
            for i in range(3)
        ]

    def test_add_period_group(self) -> None:
        """Тестирование функции `add_period_group`."""
        with patch.object(
            self.superuser,
            'has_perm',
            lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, self._add_period_group)
        actual_period_group = self._add_period_group()
        expected_period_group = PeriodGroup.objects.get(name='Period group')
        self.assertEqual(expected_period_group, actual_period_group)

    def test_copy_period_groups(self) -> None:
        """Тестирование функции `copy_period_groups`."""
        with patch.object(
            self.superuser,
            'has_perm',
            lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, self._copy_period_groups)
        copy_group = self._copy_period_groups()
        for (copy, verify) in zip(copy_group, self.selected_period_groups):
            self.assertEqual(copy.name, verify.name)

    def test_change_period_group_privileges(self) -> None:
        """Тестирование функции `change_period_group_privileges`."""
        with patch.object(
            self.superuser,
            'has_perm',
            lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, self._change_period_group_privileges)
        self.assertEqual(
            self.privileges,
            self._change_period_group_privileges(),
        )
        self.assertEqual(set(self.privileges), set(self.privileges_period_group.privileges.all()))

    def test_delete_period_groups(self) -> None:
        """Тестирование функции `delete_period_groups`."""
        with patch.object(
            self.superuser,
            'has_perm',
            lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, self._delete_period_groups)
        self.assertEqual(None, self._delete_period_groups())
        self.assertEqual(
            set(self.groups_to_delete[1:]),
            set(self.period_to_delete_groups.periodgroup_set.all())
        )

    def _add_period_group(self) -> PeriodGroup:
        """Вызов функции `add_period_group`."""
        return add_period_group(user=self.superuser, name='Period group', period_id=self.period.id)

    def _copy_period_groups(self) -> list[PeriodGroup]:
        """Вызов функции `copy_period_groups`."""
        return copy_period_groups(
            user=self.superuser,
            period_id=self.period.id,
            period_group_ids=[pg.id for pg in self.selected_period_groups],
            selected_period_id=self.selected_period.id
        )

    def _change_period_group_privileges(self) -> list[Privilege]:
        """Вызов функции `change_period_group_privileges.`"""
        return change_period_group_privileges(
            user=self.superuser,
            period_group_id=self.privileges_period_group.id,
            privileges_ids=[p.id for p in self.privileges]
        )

    def _delete_period_groups(self) -> None:
        """Вызов функции `delete_period_groups`."""
        return delete_period_groups(user=self.superuser, period_group=self.groups_to_delete[0])


class PeriodUserTestCase(TestCase):
    """Тестирование пользователей периода."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.organization_content_type = ContentType.objects.get_for_model(Organization)

        self.project = Project.objects.create(user=self.superuser, content_type=self.organization_content_type)
        self.period = Period.objects.create(name='Period', user=self.superuser, project=self.project)
        self.period_groups = [
            PeriodGroup.objects.create(name=f'Period group {i}', period=self.period) for i in range(3)
        ]

        self.privileges = [Privilege.objects.create(name=f'Privilege {i}', key=f'privilege_{i}') for i in range(3)]

    def test_change_user_period_groups(self) -> None:
        """Тестирование функции `change_user_period_groups`."""
        with patch.object(
            self.superuser,
            'has_perm',
            lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, self._change_user_period_groups)
        self.assertEqual(self.period_groups, self._change_user_period_groups())
        self.assertEqual(
            set(self.period_groups),
            set(self.user.periodgroup_set.all()),
        )

    def test_change_user_period_privileges(self) -> None:
        """Тестирование функции `change_user_period_privileges`."""
        with patch.object(
            self.superuser,
            'has_perm',
            lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, self._change_user_period_privileges)
        self.assertEqual(self.privileges, self._change_user_period_privileges())
        self.assertEqual(
            set(self.privileges),
            set(p.privilege for p in self.user.periodprivilege_set.filter(period=self.period))
        )

    def _change_user_period_groups(self) -> list[PeriodGroup]:
        """Вызов функции `change_user_period_groups`."""
        return change_user_period_groups(
            permission_user=self.superuser,
            user=self.user,
            period_group_ids=[pg.id for pg in self.period_groups]
        )

    def _change_user_period_privileges(self) -> list[Privilege]:
        """Вызов функции `change_user_period_privileges`."""
        return change_user_period_privileges(
            user=self.superuser,
            user_id=self.user.id,
            period_id=self.period.id,
            privileges_ids=[p.id for p in self.privileges]
        )


class PeriodOrganizationsHasNotDocumentTestCase(TestCase):
    """Тестирование организаций, у которых не поданы документы в периоде."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.admin = User.objects.create(username='admin', email='admin@gmain.com', is_superuser=True)
        self.curator = User.objects.create(username='curator', email='curator@gmail.com')
        self.extra_user = User.objects.create(username='extra_user', email='extra_user@gmail.com')

        self.organization_content_type = ContentType.objects.get_for_model(Organization)

        self.project = Project.objects.create(content_type=self.organization_content_type)
        self.period = Period.objects.create(project=self.project)

        self.filled_organizations = [Organization.objects.create(attributes='') for _ in range(3)]
        self.filled_organizations_curator = [Organization.objects.create(attributes='') for _ in range(3)]
        self.not_filled_organizations = [Organization.objects.create(attributes='') for _ in range(3)]
        self.not_filled_organizations_curator = [Organization.objects.create(attributes='') for _ in range(3)]

        for organization in [
            *self.filled_organizations,
            *self.filled_organizations_curator,
            *self.not_filled_organizations,
            *self.not_filled_organizations_curator,
        ]:
            self.period.division_set.create(object_id=organization.id)

        for organization in [*self.filled_organizations, *self.filled_organizations_curator]:
            Document.objects.create(period=self.period, object_id=organization.id)

        self.curator_group = CuratorGroup.objects.create()
        self.curator_group.users.add(self.curator)
        self.curator_group.organization.set([
            *self.filled_organizations_curator,
            *self.not_filled_organizations_curator
        ])

    def test_is_admin(self) -> None:
        """Тестирование функции `get_organizations_has_not_document`.

        Пользователь является администратором периода.
        """
        self.assertEqual(
            {*self.not_filled_organizations, *self.not_filled_organizations_curator},
            set(get_organizations_has_not_document(self.admin, self.period))
        )

    def test_is_curator(self) -> None:
        """Тестирование функции `get_organizations_has_not_document`.

        Пользователь является куратором периода.
        """
        self.assertEqual(
            set(self.not_filled_organizations_curator),
            set(get_organizations_has_not_document(self.curator, self.period))
        )

    def test_is_extra_user(self) -> None:
        """Тестирование функции `get_organizations_has_not_document`.

        Пользователь не имеет отношения к периоду.
        """
        self.assertRaises(PermissionDenied, get_organizations_has_not_document, self.extra_user, self.period)
