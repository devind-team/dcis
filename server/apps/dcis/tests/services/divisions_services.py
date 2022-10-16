"""Тесты модуля, отвечающего за работу с дивизионами."""

from unittest.mock import Mock, patch

from devind_dictionaries.models import Department, Organization
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Project
from apps.dcis.services.divisions_services import get_user_division_ids, get_user_divisions


class DivisionTestCase(TestCase):
    """Тесты модуля, отвечающего за работу с дивизионами."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.admin = User.objects.create(username='admin', email='admin@gmail.com')
        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.department = Department.objects.create(name='Тестовый департамент', user=self.admin)
        self.department.users.add(self.user)
        self.department_division = {'id': self.department.id, 'name': 'Тестовый департамент', 'model': 'department'}
        self.organization = Organization.objects.create(name='Тестовая организация', attributes='', user=self.admin)
        self.organization.users.add(self.user)
        self.organization_division = {
            'id': self.organization.id,
            'name': 'Тестовая организация',
            'model': 'organization',
        }
        self.department_project = Project.objects.create(
            name='Тестовый проект департамента',
            content_type=ContentType.objects.get_for_model(Department),
        )
        self.organization_project = Project.objects.create(
            name='Тестовый проект организации',
            content_type=ContentType.objects.get_for_model(Organization),
        )

    def test_get_user_divisions_without_project(self) -> None:
        """Тестирование функции `get_user_divisions` без проекта."""
        for user in (self.admin, self.user,):
            with self.subTest(user=user):
                self.assertListEqual(
                    [self.department_division, self.organization_division],
                    get_user_divisions(user)
                )

    def test_get_user_divisions_with_project(self) -> None:
        """Тестирование функции `get_user_divisions` с проектом."""
        for user in (self.admin, self.user,):
            for project_obj, division in (
                (self.department_project, self.department_division),
                (self.organization_project, self.organization_division),
            ):
                for project in (project_obj, project_obj.id, str(project_obj.id)):
                    with self.subTest(user=user, project_name=project_obj.name, project=project):
                        self.assertListEqual([division], get_user_divisions(user, project))

    def test_get_user_division_ids(self) -> None:
        """Тестирование функции `get_user_division_ids`."""
        with patch(
            'apps.dcis.services.divisions_services.get_user_divisions',
            new=Mock(return_value=[self.department_division, self.organization_division])
        ) as mock:
            user_division_ids = get_user_division_ids(self.admin, self.department_project)
            mock.assert_called_once_with(self.admin, self.department_project)
            self.assertDictEqual({
                'department': [self.department.id],
                'organization': [self.organization.id],
            }, user_division_ids)
