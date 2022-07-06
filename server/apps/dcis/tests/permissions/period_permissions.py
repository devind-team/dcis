"""Тесты разрешений на работу с периодами проектов."""

from typing import Type
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from devind_helpers.permissions import BasePermission
from django.contrib.contenttypes.models import ContentType

from apps.dcis.models import Document, Period, Project
from apps.dcis.permissions.period_permissions import (
    AddPeriod,
    ChangePeriod,
    ChangePeriodDivisions,
    ChangePeriodSettings,
    ChangePeriodSheet,
    ChangePeriodUsers,
    DeletePeriod,
    ViewPeriod,
)
from .common import PermissionsTestCase


class PeriodPermissionsTestCase(PermissionsTestCase):
    """Тесты разрешений на работу с периодами проектов."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        super().setUp()

        self.department_content_type = ContentType.objects.get_for_model(Department)

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
            self.assertFalse(AddPeriod.has_object_permission(self.context_mock, self.period))
            self.assertTrue(AddPeriod.has_object_permission(self.context_mock, self.user_project))

    def test_change_period(self) -> None:
        """Тестирование класса `ChangePeriod`."""
        self._test_change_period(ChangePeriod, 'dcis.change_period', 'change_period')

    def test_change_period_divisions(self) -> None:
        """Тестирование класса `ChangePeriodDivisions.`"""
        self._test_change_period(ChangePeriodDivisions, 'dcis.change_period', 'change_period')
        with patch(
            'apps.dcis.permissions.period_permissions.ChangePeriodBase.has_object_permission',
            new=Mock(return_value=False),
        ), patch(
            'apps.dcis.permissions.period_permissions.has_privilege',
            new=Mock(return_value=True),
        ) as mock:
            self.assertTrue(
                ChangePeriodDivisions.has_object_permission(self.context_mock, self.user_period_without_documents)
            )
            mock.assert_called_once_with(self.user.id, self.user_period_without_documents.id, 'change_period_divisions')

    def test_change_period_users(self) -> None:
        """Тестирование класса `ChangePeriodUsers`."""
        self._test_change_period(ChangePeriodUsers, 'dcis.change_period', 'change_period')
        with patch(
            'apps.dcis.permissions.period_permissions.ChangePeriodBase.has_object_permission',
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
        self._test_change_period(ChangePeriodSettings, 'dcis.change_period', 'change_period')
        with patch(
            'apps.dcis.permissions.period_permissions.ChangePeriodBase.has_object_permission',
            new=Mock(return_value=False)
        ), patch(
            'apps.dcis.permissions.period_permissions.has_privilege',
            new=Mock(return_value=True),
        ) as mock:
            self.assertTrue(
                ChangePeriodSettings.has_object_permission(self.context_mock, self.user_period_without_documents)
            )
            mock.assert_called_once_with(self.user.id, self.user_period_without_documents.id, 'change_period_settings')

    def test_change_period_sheet(self) -> None:
        """Тестирование класса `ChangePeriodSheet`."""
        self._test_change_period(ChangePeriodSheet, 'dcis.change_sheet', 'change_sheet')

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

    def _test_change_period(self, cls: Type[BasePermission], permission: str, privilege: str) -> None:
        """Тестирование разрешений на изменение периода."""
        self.assertFalse(cls.has_object_permission(self.context_mock, self.period))
        self.assertFalse(cls.has_object_permission(self.context_mock, self.user_period_without_documents))
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == permission):
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
            mock.assert_called_once_with(self.user.id, self.user_period_without_documents.id, privilege)
