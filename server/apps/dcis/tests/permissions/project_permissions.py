"""Тесты разрешений на работу с проектами сборов."""

from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied

from apps.dcis.models import Period, Project
from apps.dcis.permissions.project_permissions import can_change_project, can_delete_project, can_view_project
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

    def test_can_view_project(self) -> None:
        """Тестирование функции `can_view_project`."""
        self.assertRaises(PermissionDenied, can_view_project, self.user, self.project)
        can_view_project(self.user, self.user_project_without_periods)

    def test_can_change_project(self) -> None:
        """Тестирование функции `can_change_project`."""
        self.assertRaises(PermissionDenied, can_change_project, self.user, self.project)
        self.assertRaises(PermissionDenied, can_change_project, self.user, self.user_project_without_periods)
        with patch(
                'apps.dcis.permissions.project_permissions.can_view_project',
                new=Mock()
        ):
            self.assertRaises(PermissionDenied, can_change_project, self.user, self.project)
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.change_project'):
                can_change_project(self.user, self.project)
            self.assertRaises(PermissionDenied, can_change_project, self.user,
                              self.user_project_without_periods)
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.add_project'):
                can_change_project(self.user, self.user_project_without_periods)

    def test_can_delete_project(self) -> None:
        """Тестирование функции `can_delete_project`."""
        self.assertRaises(PermissionDenied, can_delete_project, self.user, self.project)
        self.assertRaises(PermissionDenied, can_delete_project, self.user, self.user_project_without_periods)
        self.assertRaises(PermissionDenied, can_delete_project, self.user, self.user_project_with_periods)
        with patch(
                'apps.dcis.permissions.project_permissions.can_view_project',
                new=Mock()
        ):
            self.assertRaises(PermissionDenied, can_delete_project, self.user, self.project)
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.delete_project'):
                can_delete_project(self.user, self.project)
            self.assertRaises(PermissionDenied, can_delete_project, self.user,
                              self.user_project_without_periods)
            self.assertRaises(PermissionDenied, can_delete_project, self.user, self.user_project_with_periods)
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.add_project'):
                can_delete_project(self.user, self.user_project_without_periods)
                self.assertRaises(
                    PermissionDenied,
                    can_delete_project,
                    self.user,
                    self.user_project_with_periods
                )
