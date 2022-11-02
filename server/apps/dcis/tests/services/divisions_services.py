"""Тесты модуля, отвечающего за работу с дивизионами."""

from unittest.mock import Mock, patch

from devind_dictionaries.models import Department, Organization
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Document, Period, Project
from apps.dcis.services.divisions_services import (
    get_user_division_ids,
    get_user_divisions,
    is_document_division_member,
    is_period_division_member,
)


class DivisionTestCase(TestCase):
    """Тесты модуля, отвечающего за работу с дивизионами."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.organization_content_type = ContentType.objects.get_for_model(Organization)

        self.admin = User.objects.create(username='admin', email='admin@gmail.com')
        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.period_division_member = User.objects.create(
            username='period_division_member',
            email='period_division_member@gmail.com',
        )
        self.document_division_member = User.objects.create(
            username='document_division_member',
            email='document_division_member@gmail.com',
        )
        self.extra_user = User.objects.create(username='extra_user', email='extra_user@gmail.com')

        self.department = Department.objects.create(name='Тестовый департамент', user=self.admin)
        self.department.users.add(self.user)
        self.department_division = {'id': self.department.id, 'name': 'Тестовый департамент', 'model': 'department'}

        self.organization = Organization.objects.create(name='Тестовая организация', attributes='', user=self.admin)
        self.organization_child = Organization.objects.create(
            name='Дочерняя тестовая организация',
            attributes='',
            parent=self.organization
        )
        self.organization.users.add(self.user)
        self.organization_division = {
            'id': self.organization.id,
            'name': 'Тестовая организация',
            'model': 'organization',
        }
        self.organization_child_division = {
            'id': self.organization_child.id,
            'name': 'Дочерняя тестовая организация',
            'model': 'organization'
        }

        self.department_project = Project.objects.create(content_type=self.department_content_type)
        self.organization_project = Project.objects.create(content_type=self.organization_content_type)

        self.period_division_member_project = Project.objects.create(content_type=self.organization_content_type)
        self.period_division_member_period = Period.objects.create(project=self.period_division_member_project)
        self.period_division_member_organization = Organization.objects.create(attributes='')
        self.period_division_member_organization.users.add(self.period_division_member)
        self.period_division_member_period.division_set.create(object_id=self.period_division_member_organization.id)

        self.document_division_member_project = Project.objects.create(content_type=self.organization_content_type)
        self.document_division_member_period_not_multiple = Period.objects.create(
            project=self.document_division_member_project,
            multiple=False
        )
        self.document_division_member_period_multiple = Period.objects.create(
            project=self.document_division_member_project,
            multiple=True
        )
        self.document_division_member_organization = Organization.objects.create(attributes='')
        self.document_division_member_organization.users.add(self.document_division_member)
        self.document_division_member_period_not_multiple.division_set.create(
            object_id=self.document_division_member_organization.id,
        )
        self.document_division_member_multiple_not_division_document = Document.objects.create(
            period=self.document_division_member_period_multiple,
        )
        self.document_division_member_multiple_division_document = Document.objects.create(
            period=self.document_division_member_period_multiple,
            object_id=self.document_division_member_organization.id,
        )
        self.document_division_member_not_multiple_document = Document.objects.create(
            period=self.document_division_member_period_not_multiple,
        )

    def test_get_user_divisions_without_project(self) -> None:
        """Тестирование функции `get_user_divisions` без проекта."""
        for user in (self.admin, self.user,):
            with self.subTest(user=user):
                self.assertListEqual(
                    [self.department_division, self.organization_division, self.organization_child_division],
                    get_user_divisions(user)
                )

    def test_get_user_divisions_with_project(self) -> None:
        """Тестирование функции `get_user_divisions` с проектом."""
        for user in (self.admin, self.user,):
            for project_obj, divisions in (
                (self.department_project, [self.department_division]),
                (self.organization_project, [self.organization_division, self.organization_child_division]),
            ):
                for project in (project_obj, project_obj.id, str(project_obj.id)):
                    with self.subTest(user=user, project_name=project_obj.name, project=project):
                        self.assertListEqual(divisions, get_user_divisions(user, project))

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

    def test_is_period_division_member(self) -> None:
        """Тестирование функции `is_period_division_member`."""
        self.assertFalse(is_period_division_member(self.extra_user, self.period_division_member_period))
        self.assertTrue(is_period_division_member(self.period_division_member, self.period_division_member_period))

    def test_is_document_division_member(self) -> None:
        """Тестирование функции `is_document_division_member`."""
        for document in [
            self.document_division_member_multiple_division_document,
            self.document_division_member_not_multiple_document
        ]:
            self.assertFalse(is_document_division_member(self.extra_user, document))
            self.assertTrue(is_document_division_member(self.document_division_member, document))
        self.assertFalse(is_document_division_member(
            self.extra_user,
            self.document_division_member_multiple_not_division_document,
        ))
        self.assertFalse(is_document_division_member(
            self.document_division_member,
            self.document_division_member_multiple_not_division_document,
        ))
