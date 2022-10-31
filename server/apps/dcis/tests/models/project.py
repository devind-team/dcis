"""Тесты моделей проекта."""
from unittest import TestCase

from devind_dictionaries.models import Department, Organization
from django.contrib.contenttypes.models import ContentType

from apps.dcis.models import Project


class ProjectModelTestCase(TestCase):
    """Тестирование модели `Project`."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.organization_content_type = ContentType.objects.get_for_model(Organization)

        self.department_project = Project.objects.create(content_type=self.department_content_type)
        self.organization_project = Project.objects.create(content_type=self.organization_content_type)

    def test_division_name(self) -> None:
        """Тестирование свойства `division_name`."""
        self.assertEqual('department', self.department_project.division_name)
        self.assertEqual('organization', self.organization_project.division_name)

    def test_division(self) -> None:
        """Тестирование свойства `division`."""
        self.assertEqual(Department, self.department_project.division)
        self.assertEqual(Organization, self.organization_project.division)
