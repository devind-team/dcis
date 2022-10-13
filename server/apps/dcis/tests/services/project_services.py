"""Тесты модуля, отвечающего за работу с проектами."""
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department, Organization
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Division, Period, PeriodGroup, PeriodPrivilege, Privilege, Project
from apps.dcis.permissions.project_permissions import can_add_project, can_change_project, can_delete_project
from apps.dcis.services.project_services import (
    change_project, create_project,
    delete_project, get_user_divisions_projects,
    get_user_participant_projects,
    get_user_privileges_projects,
    get_user_projects,
)


class GetUserProjectsTestCase(TestCase):
    """Тестирование получения проектов пользователя."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.organization_content_type = ContentType.objects.get_for_model(Organization)

        self.user = User.objects.create(username='user', email='user@gmain.com')
        self.super_user = User.objects.create(username='super_user', email='super_user@gmain.com', is_superuser=True)
        self.extra_user = User.objects.create(username='extra_user', email='extra_user@gmail.com')

        self.user_projects = [Project.objects.create(
            user=self.user, content_type=self.department_content_type
        ) for _ in range(3)]
        self.user_projects_invisible = [Project.objects.create(
            user=self.user, content_type=self.department_content_type, visibility=False
        ) for _ in range(3)]

        self.user_period_projects = [Project.objects.create(
            content_type=self.department_content_type
        ) for _ in range(3)]
        self.user_periods = [Period.objects.create(
            user=self.user, project=project
        ) for project in self.user_period_projects]
        self.user_period_projects_invisible = [Project.objects.create(
            content_type=self.department_content_type, visibility=False
        ) for _ in range(3)]
        self.user_periods_invisible = [Period.objects.create(
            user=self.user, project=project
        ) for project in self.user_period_projects_invisible]

        self.user_group_projects = [Project.objects.create(
            content_type=self.department_content_type
        ) for _ in range(3)]
        self.user_group_periods = [Period.objects.create(project=project) for project in self.user_group_projects]
        self.user_group_projects_invisible = [Project.objects.create(
            content_type=self.department_content_type, visibility=False
        ) for _ in range(3)]
        self.user_group_periods_invisible = [Period.objects.create(
            project=project
        ) for project in self.user_group_projects_invisible]
        for period in [*self.user_group_periods, *self.user_group_periods_invisible]:
            period_group = PeriodGroup.objects.create(period=period)
            period_group.users.add(self.user)

        self.privilege = Privilege.objects.create()
        self.privilege_project = Project.objects.create(content_type=self.department_content_type)
        self.privilege_period = Period.objects.create(project=self.privilege_project)
        self.privilege_project_invisible = Project.objects.create(
            content_type=self.department_content_type,
            visibility=False
        )
        self.privilege_period_invisible = Period.objects.create(project=self.privilege_project_invisible)
        for period in [self.privilege_period, self.privilege_period_invisible]:
            PeriodPrivilege.objects.create(
                period=period,
                user=self.user,
                privilege=self.privilege,
            )

        self.department = Department.objects.create(user=self.user)
        self.department_project = Project.objects.create(content_type=self.department_content_type)
        self.department_period = Period.objects.create(project=self.department_project)
        self.department_division = Division.objects.create(period=self.department_period, object_id=self.department.id)
        self.department_project_invisible = Project.objects.create(
            content_type=self.department_content_type,
            visibility=False
        )
        self.department_period_invisible = Period.objects.create(project=self.department_project_invisible)
        self.department_division_invisible = Division.objects.create(
            period=self.department_period_invisible,
            object_id=self.department.id
        )

        self.organization = Organization.objects.create(attributes='', user=self.user)
        self.organization_project = Project.objects.create(content_type=self.organization_content_type)
        self.organization_period = Period.objects.create(project=self.organization_project)
        self.organization_division = Division.objects.create(
            period=self.organization_period,
            object_id=self.organization.id,
        )

        self.extra_project = Project.objects.create(content_type=self.department_content_type)

    def test_get_user_participant_projects(self) -> None:
        """Тестирование функции `get_user_participant_projects`."""
        self.assertSetEqual(
            {*self.user_projects, *self.user_projects_invisible, *self.user_period_projects, *self.user_group_projects},
            set(get_user_participant_projects(self.user)),
        )

    def test_get_user_privileges_projects(self) -> None:
        """Тестирование функции `get_user_privileges_projects`."""
        self.assertSetEqual(
            {self.privilege_project},
            set(get_user_privileges_projects(self.user)),
        )

    def test_get_user_divisions_projects_without_projects(self) -> None:
        """Тестирование функции `get_user_divisions_projects` для пользователя, у которого нет проектов."""
        self.assertQuerysetEqual(
            Project.objects.none(),
            get_user_divisions_projects(self.extra_user)
        )

    def test_get_user_divisions_projects_with_projects(self) -> None:
        """Тестирование функции `get_user_divisions_projects` для пользователя, у которого есть проекты."""
        self.assertSetEqual(
            {self.department_project, self.organization_project},
            set(get_user_divisions_projects(self.user)),
        )

    def test_get_user_projects_with_perm(self) -> None:
        """Тестирование функции `get_user_projects` при наличии у пользователя разрешения `dcis.view_project`."""
        with patch.object(self.user, 'has_perm', new=Mock(return_value=True)) as mock:
            projects = get_user_projects(self.user)
            mock.assert_called_once_with('dcis.view_project')
            self.assertQuerysetEqual(Project.objects.all(), projects)

    def test_get_user_projects_without_perm(self) -> None:
        """Тестирование функции `get_user_projects` при отсутствии у пользователя разрешения `dcis.view_project`."""
        self.assertSetEqual(
            {
                *self.user_projects,
                *self.user_projects_invisible,
                *self.user_period_projects,
                *self.user_group_projects,
                self.department_project,
                self.organization_project,
                self.privilege_project,
            },
            set(get_user_projects(self.user)),
        )


class ProjectTestCase(TestCase):
    """Тестирование проекта и прав."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.organization_content_type = ContentType.objects.get_for_model(Organization)
        self.super_user = User.objects.create(username='super_user', email='super_user@gmain.com', is_superuser=True)
        self.data_project = {
            'name': 'Testing name',
            'short': 'Testing short',
            'description': 'Description project',
            'content_type': self.organization_content_type
        }
        self.project = Project.objects.create(
            name='Testing name 2',
            short='Testing short 2',
            description='Description project 2',
            content_type=ContentType.objects.get_for_model(
                Project.DIVISION_KIND.get(self.organization_content_type, Department)
            ),
            visibility=True,
            archive=True
        )

    def test_create_project(self) -> None:
        """Тестирование функции `create_project`."""
        with patch.object(self.super_user, 'has_perm', new=lambda perm: perm != 'dcis.add_project'):
            self.assertRaises(PermissionDenied, can_add_project, self.super_user)
        self.assertEqual(
            create_project(self.super_user, self.data_project, True),
            Project.objects.get(name=self.data_project['name']),
            'Create project'
        )

    def test_change_project(self) -> None:
        """Тестирование функции `change_project`."""
        with patch.object(self.super_user, 'has_perm', new=lambda perm: perm != 'dcis.change_project'):
            self.assertRaises(PermissionDenied, can_change_project, self.super_user, self.project)
        self.assertEqual(
            change_project(
                user=self.super_user,
                project=self.project,
                name='Change name',
                short='Change short',
                description='Change description',
                visibility=False,
                archive=False
            ),
            Project.objects.get(name='Change name'),
            'Change project'
        )

    def test_delete_project(self) -> None:
        """Тестирование функции `delete_project`."""
        with patch.object(self.super_user, 'has_perm', new=lambda perm: perm != 'dcis.delete_project'):
            self.assertRaises(PermissionDenied, can_delete_project, self.super_user, self.project)
        self.assertEqual(
            delete_project(user=self.super_user, project=self.project),
            None,
            'Delete project'
        )
