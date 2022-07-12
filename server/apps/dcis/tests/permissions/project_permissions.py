"""Тесты разрешений на работу с проектами сборов."""

from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType

from apps.dcis.models import Period, Project
from apps.dcis.permissions.project_permissions import ChangeProject, DeleteProject, ViewProject
from .common import PermissionsTestCase


class ProjectPermissionsTestCase(PermissionsTestCase):
    """Тесты разрешений на работу с проектами сборов."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        super().setUp()

        self.department_content_type = ContentType.objects.get_for_model(Department)

        self.project = Project.objects.create(content_type=self.department_content_type)

        self.user_project_without_periods = Project.objects.create(
            user=self.user,
            content_type=self.department_content_type
        )

        self.user_project_with_periods = Project.objects.create(
            user=self.user,
            content_type=self.department_content_type
        )
        self.periods = [Period.objects.create(project=self.user_project_with_periods) for _ in range(3)]

    def test_view_project(self) -> None:
        """Тестирование класса `ViewProject`."""
        self.assertFalse(ViewProject.has_object_permission(self.context_mock, self.project))
        self.assertTrue(ViewProject.has_object_permission(self.context_mock, self.user_project_without_periods))

    def test_change_project(self) -> None:
        """Тестирование класса `ChangeProject`."""
        self.assertFalse(ChangeProject.has_object_permission(self.context_mock, self.project))
        self.assertFalse(ChangeProject.has_object_permission(self.context_mock, self.user_project_without_periods))
        with patch(
            'apps.dcis.permissions.project_permissions.ViewProject.has_object_permission',
            new=Mock(return_value=True)
        ):
            self.assertFalse(ChangeProject.has_object_permission(self.context_mock, self.project))
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.change_project'):
                self.assertTrue(ChangeProject.has_object_permission(self.context_mock, self.project))
            self.assertFalse(ChangeProject.has_object_permission(self.context_mock, self.user_project_without_periods))
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.add_project'):
                self.assertTrue(
                    ChangeProject.has_object_permission(self.context_mock, self.user_project_without_periods)
                )

    def test_delete_project(self) -> None:
        """Тестирование класса `DeleteProject`."""
        self.assertFalse(DeleteProject.has_object_permission(self.context_mock, self.project))
        self.assertFalse(DeleteProject.has_object_permission(self.context_mock, self.user_project_without_periods))
        self.assertFalse(DeleteProject.has_object_permission(self.context_mock, self.user_project_with_periods))
        with patch(
            'apps.dcis.permissions.project_permissions.ViewProject.has_object_permission',
            new=Mock(return_value=True)
        ):
            self.assertFalse(DeleteProject.has_object_permission(self.context_mock, self.project))
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.delete_project'):
                self.assertTrue(DeleteProject.has_object_permission(self.context_mock, self.project))
            self.assertFalse(DeleteProject.has_object_permission(self.context_mock, self.user_project_without_periods))
            self.assertFalse(DeleteProject.has_object_permission(self.context_mock, self.user_project_with_periods))
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.add_project'):
                self.assertTrue(
                    DeleteProject.has_object_permission(self.context_mock, self.user_project_without_periods)
                )
                self.assertFalse(DeleteProject.has_object_permission(self.context_mock, self.user_project_with_periods))
