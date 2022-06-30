"""Тесты разрешений на работу с периодами проектов."""

from typing import Type
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Document, Period, Project
from apps.dcis.permissions.period_permissions import (
    AddPeriod,
    ChangePeriod,
    ChangePeriodDivisions,
    ChangePeriodSettings,
    ChangePeriodUsers,
    DeletePeriod,
    ViewPeriod,
)


class PeriodPermissionsTestCase(TestCase):
    """Тесты разрешений на работу с периодами проектов."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.department_content_type = ContentType.objects.get_for_model(Department)

        self.user = User.objects.create(username='user', email='user@gmail.com')

        self.context_mock = Mock()
        self.context_mock.user = self.user

        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)

        self.user_project = Project.objects.create(user=self.user, content_type=self.department_content_type)
        self.user_period_without_documents = Period.objects.create(user=self.user, project=self.user_project)
        self.user_period_with_documents = Period.objects.create(user=self.user, project=self.user_project)
        self.document = Document.objects.create(period=self.user_period_with_documents)

    def test_view_period(self) -> None:
        """Тестирование класса `ViewPeriod`."""
        self.assertFalse(ViewPeriod.has_object_permission(self.context_mock, self.period))
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.view_project'):
            self.assertFalse(ViewPeriod.has_object_permission(self.context_mock, self.period))
        self.assertTrue(ViewPeriod.has_object_permission(self.context_mock, self.user_period_without_documents))

    def test_add_period(self) -> None:
        """Тестирование класса `AddPeriod`."""
        self.assertFalse(AddPeriod.has_object_permission(self.context_mock, self.project))
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.view_project'):
            self.assertFalse(AddPeriod.has_object_permission(self.context_mock, self.project))
        with patch.object(self.user, 'has_perm', new=lambda perm: perm in ('dcis.view_project', 'dcis.add_period')):
            self.assertTrue(AddPeriod.has_object_permission(self.context_mock, self.project))
        self.assertFalse(AddPeriod.has_object_permission(self.context_mock, self.user_project))
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.add_project'):
            self.assertTrue(AddPeriod.has_object_permission(self.context_mock, self.user_project))

    def test_change_period(self) -> None:
        """Тестирование класса `ChangePeriod`."""
        self._test_change_period(ChangePeriod)

    def test_change_period_divisions(self) -> None:
        """Тестирование класса `ChangePeriodDivisions.`"""
        self._test_change_period(ChangePeriodDivisions)
        with patch(
            'apps.dcis.permissions.period_permissions.ChangePeriod.has_object_permission',
            new=Mock(return_value=False),
        ), patch(
            'apps.dcis.permissions.period_permissions.has_privilege',
            new=Mock(return_value=True),
        ) as mock:
            self.assertTrue(ChangePeriodDivisions.has_object_permission(self.context_mock, self.user_period_without_documents))
            mock.assert_called_once_with(self.user.id, self.user_period_without_documents.id, 'change_period_divisions')

    def test_change_period_users(self) -> None:
        """Тестирование класса `ChangePeriodUsers`."""
        self._test_change_period(ChangePeriodUsers)
        with patch(
            'apps.dcis.permissions.period_permissions.ChangePeriod.has_object_permission',
            new=Mock(return_value=False),
        ), patch(
            'apps.dcis.permissions.period_permissions.has_privilege',
            new=Mock(return_value=True),
        ) as mock:
            self.assertTrue(
                ChangePeriodUsers.has_object_permission(self.context_mock, self.user_period_without_documents)
            )
            mock.assert_called_once_with(self.user.id, self.user_period_without_documents.id, 'change_period_users')

    def test_change_period_settings(self) -> None:
        """Тестирование класса `ChangePeriodSettings`."""
        self._test_change_period(ChangePeriodSettings)
        with patch(
            'apps.dcis.permissions.period_permissions.ChangePeriod.has_object_permission',
            new=Mock(return_value=False)
        ), patch(
            'apps.dcis.permissions.period_permissions.has_privilege',
            new=Mock(return_value=True),
        ) as mock:
            self.assertTrue(
                ChangePeriodSettings.has_object_permission(self.context_mock, self.user_period_without_documents)
            )
            mock.assert_called_once_with(self.user.id, self.user_period_without_documents.id, 'change_period_settings')

    def test_delete_period(self) -> None:
        """Тестирование класса `DeletePeriod`."""
        self.assertFalse(DeletePeriod.has_object_permission(self.context_mock, self.period))
        self.assertFalse(DeletePeriod.has_object_permission(self.context_mock, self.user_period_without_documents))
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.delete_period'):
            self.assertTrue(DeletePeriod.has_object_permission(self.context_mock, self.user_period_without_documents))
        with patch(
            'apps.dcis.permissions.period_permissions.ViewPeriod.has_object_permission',
            new=Mock(return_value=True),
        ):
            for global_perm in ('dcis.add_project', 'dcis.add_period'):
                with patch.object(self.user, 'has_perm', new=lambda perm: perm == global_perm):
                    self.assertFalse(DeletePeriod.has_object_permission(self.context_mock, self.period))
                    self.assertFalse(
                        DeletePeriod.has_object_permission(self.context_mock, self.user_period_with_documents)
                    )
                    self.assertTrue(
                        DeletePeriod.has_object_permission(self.context_mock, self.user_period_without_documents)
                    )

    def _test_change_period(self, cls: Type[ChangePeriod]) -> None:
        """Тестирование разрешений на изменение периода."""
        self.assertFalse(cls.has_object_permission(self.context_mock, self.period))
        self.assertFalse(cls.has_object_permission(self.context_mock, self.user_period_without_documents))
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.change_period'):
            self.assertTrue(cls.has_object_permission(self.context_mock, self.user_period_without_documents))
        with patch.object(
            self.user, 'has_perm', new=lambda perm: perm == 'dcis.add_project'
        ), patch(
            'apps.dcis.permissions.period_permissions.ViewPeriod.has_object_permission',
            new=Mock(return_value=True),
        ):
            self.assertFalse(cls.has_object_permission(self.context_mock, self.period))
            self.assertTrue(cls.has_object_permission(self.context_mock, self.user_period_without_documents))
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.add_period'):
            self.assertTrue(cls.has_object_permission(self.context_mock, self.user_period_without_documents))
        with patch('apps.dcis.permissions.period_permissions.has_privilege', new=Mock(return_value=True)) as mock:
            self.assertTrue(cls.has_object_permission(self.context_mock, self.user_period_without_documents))
            mock.assert_called_once_with(self.user.id, self.user_period_without_documents.id, 'change_period')
