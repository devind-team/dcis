"""Тестирование модуля, отвечающий за работу с кураторами."""
from devind_dictionaries.models import Department, Organization
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import CuratorGroup, Document, Period, Project
from apps.dcis.services.curator_services import get_curator_groups, get_curator_organizations, is_document_curator


class CuratorTestCase(TestCase):
    """Тестирование модуля, отвечающего за работу с кураторами."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.group_user = User.objects.create(username='group_user', email='group_user@gmail.com')

        self.curator_groups = [CuratorGroup.objects.create(name=f'Кураторская группа №{i}') for i in range(3)]
        self.extra_curator_groups = CuratorGroup.objects.create(name='Кураторская группа №3')
        self.organizations = [Organization.objects.create(name=f'Организация №{i}', attributes='') for i in range(3)]
        for curator_group, organization in zip(self.curator_groups, self.organizations):
            curator_group.users.add(self.group_user)
            curator_group.organization.add(organization)

        self.department_project = Project.objects.create(content_type=ContentType.objects.get_for_model(Department))
        self.department_period = Period.objects.create(project=self.department_project)
        self.department_document = Document.objects.create(period=self.department_period)

        self.organization_project = Project.objects.create(content_type=ContentType.objects.get_for_model(Organization))

        self.organization_multiple_period = Period.objects.create(multiple=True, project=self.organization_project)
        self.organization_multiple_document = Document.objects.create(period=self.organization_multiple_period)
        self.organization_multiple_user_document = Document.objects.create(
            period=self.organization_multiple_period,
            object_id=self.organizations[0].id
        )

        self.organization_period = Period.objects.create(project=self.organization_project)
        self.organization_document = Document.objects.create(period=self.organization_period)
        self.organization_period.division_set.create(object_id=self.organizations[0].id)

    def test_get_curator_groups(self) -> None:
        """Тестирование функции `get_curator_groups`."""
        self.assertEqual(self.curator_groups, list(get_curator_groups(self.group_user)))
        self.assertEqual([], list(get_curator_groups(self.user)))

    def test_get_curator_organizations(self) -> None:
        """Тестирование функции `get_curator_organizations`."""
        self.assertEqual(self.organizations, list(get_curator_organizations(self.group_user)))
        self.assertEqual([], list(get_curator_organizations(self.user)))

    def test_is_document_curator(self) -> None:
        """Тестирование функции `is_document_curator`."""
        self.assertFalse(is_document_curator(self.group_user, self.department_document))
        self.assertFalse(is_document_curator(self.user, self.organization_multiple_document))
        self.assertFalse(is_document_curator(self.group_user, self.organization_multiple_document))
        self.assertFalse(is_document_curator(self.user, self.organization_multiple_user_document))
        self.assertTrue(is_document_curator(self.group_user, self.organization_multiple_user_document))
        self.assertFalse(is_document_curator(self.user, self.organization_document))
        self.assertTrue(is_document_curator(self.group_user, self.organization_document))
