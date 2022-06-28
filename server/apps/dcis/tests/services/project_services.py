"""Тесты модуля, отвечающего за работу с проектами."""

from unittest.mock import Mock, patch

from devind_dictionaries.models import Department, Organization
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Division, Period, PeriodGroup, PeriodPrivilege, Privilege, Project
from apps.dcis.services.project_services import (
    get_user_divisions_projects,
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

        self.user_projects = [Project.objects.create(
            user=self.user, content_type=self.department_content_type
        ) for _ in range(3)]

        self.user_period_projects = [Project.objects.create(
            content_type=self.department_content_type
        ) for _ in range(3)]
        self.user_periods = [Period.objects.create(
            user=self.user, project=project
        ) for project in self.user_period_projects]

        self.user_group_projects = [Project.objects.create(
            content_type=self.department_content_type
        ) for _ in range(3)]
        self.user_group_periods = [Period.objects.create(project=project) for project in self.user_group_projects]
        self.user_groups: list[PeriodGroup] = []
        for period in self.user_group_periods:
            self.user_groups.append(PeriodGroup.objects.create(period=period))
            self.user_groups[-1].users.add(self.user)

        self.privilege_project = Project.objects.create(content_type=self.department_content_type)
        self.privilege_period = Period.objects.create(project=self.privilege_project)
        self.privilege = Privilege.objects.create()
        self.period_privilege = PeriodPrivilege.objects.create(
            period=self.privilege_period,
            user=self.user,
            privilege=self.privilege,
        )
        
        self.department = Department.objects.create(user=self.user)
        self.department_project = Project.objects.create(content_type=self.department_content_type)
        self.department_period = Period.objects.create(project=self.department_project)
        self.department_division = Division.objects.create(period=self.department_period, object_id=self.department.id)

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
            {*self.user_projects, *self.user_period_projects, *self.user_group_projects},
            set(get_user_participant_projects(self.user)),
        )

    def test_get_user_privileges_projects(self) -> None:
        """Тестирование функции `get_user_privileges_projects`."""
        self.assertSetEqual(
            {self.privilege_project},
            set(get_user_privileges_projects(self.user)),
        )

    def test_get_user_divisions_projects(self) -> None:
        """Тестирование функции `get_user_divisions_projects`."""
        self.assertSetEqual(
            {self.department_project, self.organization_project},
            set(get_user_divisions_projects(self.user)),
        )

    def test_get_user_projects_with_perm(self) -> None:
        """Тестирование функции `get_user_projects` при наличии разрешения `dcis.view_project` у пользователя."""
        with patch.object(self.user, 'has_perm', new=Mock(return_value=True)) as mock:
            projects = get_user_projects(self.user)
            mock.assert_called_once_with('dcis.view_project')
            self.assertQuerysetEqual(Project.objects.all(), projects)

    def test_get_user_projects_without_perm(self) -> None:
        """Тестирование функции `get_user_projects` при отсутствии разрешения `dcis.view_project` у пользователя."""
        self.assertSetEqual(
            {
                *self.user_projects,
                *self.user_period_projects,
                *self.user_group_projects,
                self.department_project,
                self.organization_project,
                self.privilege_project,
            },
            set(get_user_projects(self.user)),
        )
