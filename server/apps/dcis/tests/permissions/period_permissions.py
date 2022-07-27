"""Тесты разрешений на работу с периодами проектов."""

from typing import Callable, Any
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied

from apps.dcis.models import Document, Period, Project
from apps.dcis.permissions.period_permissions import (
    can_add_period,
    can_change_period,
    can_change_period_divisions,
    can_change_period_groups,
    can_change_period_settings,
    can_change_period_sheet,
    can_change_period_users,
    can_delete_period,
    can_view_period,
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
        self.assertRaises(PermissionDenied, can_view_period, self.context_mock, self.period)
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.view_project'):
            self.assertRaises(PermissionDenied, can_view_period, self.context_mock, self.period)
        can_view_period(self.context_mock, self.user_period_without_documents)

    def test_add_period(self) -> None:
        """Тестирование класса `AddPeriod`."""
        self.assertRaises(PermissionDenied, can_add_period, self.context_mock, self.project)
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.view_project'):
            self.assertRaises(PermissionDenied, can_add_period, self.context_mock, self.project)
        with patch.object(self.user, 'has_perm', new=lambda perm: perm in ('dcis.view_project', 'dcis.add_period')):
            can_add_period(self.context_mock, self.project)
        self.assertRaises(PermissionDenied, can_add_period, self.context_mock, self.user_project)
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.add_project'):
            self.assertRaises(PermissionDenied, can_add_period, self.context_mock, self.period)
            can_add_period(self.context_mock, self.user_project)

    def test_change_period(self) -> None:
        """Тестирование класса `ChangePeriod`."""
        self._test_change_period(can_change_period, 'dcis.change_period', 'change_period')

    def test_change_period_divisions(self) -> None:
        """Тестирование класса `ChangePeriodDivisions.`"""
        self._test_change_period_element(
            can_change_period_divisions,
            'dcis.change_period',
            'change_period',
            'change_period_divisions',
        )

    def test_change_period_groups(self) -> None:
        """Тестирование класса `ChangePeriodGroups`."""
        self._test_change_period_element(
            can_change_period_groups,
            'dcis.change_period',
            'change_period',
            'change_period_groups',
        )

    def test_change_period_users(self) -> None:
        """Тестирование класса `ChangePeriodUsers`."""
        self._test_change_period_element(
            can_change_period_users,
            'dcis.change_period',
            'change_period',
            'change_period_users',
        )

    def test_change_period_settings(self) -> None:
        """Тестирование класса `ChangePeriodSettings`."""
        self._test_change_period_element(
            can_change_period_settings,
            'dcis.change_period',
            'change_period',
            'change_period_settings',
        )

    def test_change_period_sheet(self) -> None:
        """Тестирование класса `ChangePeriodSheet`."""
        self._test_change_period(can_change_period_sheet, 'dcis.change_sheet', 'change_sheet')

    def test_delete_period(self) -> None:
        """Тестирование класса `DeletePeriod`."""
        self.assertRaises(PermissionDenied, can_delete_period, self.context_mock, self.period)
        self.assertRaises(PermissionDenied, can_delete_period, self.context_mock, self.user_period_without_documents)
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.delete_period'):
            can_delete_period(self.context_mock, self.user_period_without_documents)
        with patch(
                'apps.dcis.permissions.period_permissions.can_view_period',
                new=Mock(return_value=True),
        ):
            for global_perm in ('dcis.add_project', 'dcis.add_period'):
                with patch.object(self.user, 'has_perm', new=lambda perm: perm == global_perm):
                    self.assertRaises(PermissionDenied, can_delete_period, self.context_mock, self.period)
                    self.assertRaises(PermissionDenied,
                                      can_delete_period, self.context_mock, self.user_period_with_documents
                                      )
                    can_delete_period(self.context_mock, self.user_period_without_documents)

    def _test_change_period(self, f: Callable[[Any, Any], None], permission: str, privilege: str) -> None:
        """Тестирование разрешений на изменение периода."""
        self.assertRaises(PermissionDenied, f, self.context_mock, self.period)
        self.assertRaises(PermissionDenied, f, self.context_mock, self.user_period_without_documents)
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == permission):
            f(self.context_mock, self.user_period_without_documents)
        with patch.object(
                self.user, 'has_perm', new=lambda perm: perm == 'dcis.add_project'
        ), patch(
            'apps.dcis.permissions.period_permissions.can_view_period',
            new=Mock(),
        ):
            self.assertRaises(PermissionDenied, f, self.context_mock, self.period)
            f(self.context_mock, self.user_period_without_documents)
        with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.add_period'):
            f(self.context_mock, self.user_period_without_documents)
        with patch('apps.dcis.permissions.period_permissions.has_privilege', new=Mock(return_value=True)) as mock:
            f(self.context_mock, self.user_period_without_documents)
            mock.assert_called_once_with(self.user.id, self.user_period_without_documents.id, privilege)

    def _test_change_period_element(
            self,
            f: Callable[[Any, Any], None],
            permission: str,
            change_period_privilege: str,
            change_period_element_privilege: str
    ) -> None:
        """Тестирование разрешений на изменение элемента периода."""
        self._test_change_period(f, permission, change_period_privilege)
        with patch(
                'apps.dcis.permissions.period_permissions.can_change_period_base',
                new=Mock(side_effect=PermissionDenied()),
        ), patch(
            'apps.dcis.permissions.period_permissions.has_privilege',
            new=Mock(return_value=True),
        ) as mock:
            f(self.context_mock, self.user_period_without_documents)
            mock.assert_called_once_with(
                self.user.id,
                self.user_period_without_documents.id,
                change_period_element_privilege
            )
