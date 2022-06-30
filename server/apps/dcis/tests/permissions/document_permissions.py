"""Тесты разрешений на работу с документами периодов."""

from typing import Type
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from devind_helpers.permissions import BasePermission
from django.contrib.contenttypes.models import ContentType

from apps.dcis.models import Document, Period, Project
from apps.dcis.permissions.document_permissions import AddDocument, ChangeDocument, DeleteDocument, ViewDocument
from .common import PermissionsTestCase


class DocumentPermissionsTestCase(PermissionsTestCase):
    """Тесты разрешений на работу с документами периодов."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        super().setUp()

        self.department_content_type = ContentType.objects.get_for_model(Department)

        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)
        self.document = Document.objects.create(period=self.period)

        self.user_project = Project.objects.create(user=self.user, content_type=self.department_content_type)
        self.user_period = Period.objects.create(user=self.user, project=self.user_project)
        self.user_document = Document.objects.create(period=self.user_period)

    def test_view_document(self) -> None:
        """Тестирование класса `ViewDocument`."""
        self.assertFalse(ViewDocument.has_object_permission(self.context_mock, self.document))
        with patch.object(self.user, 'has_perm', new=lambda perm: perm in ('dcis.view_project', 'dcis.view_period')):
            self.assertFalse(ViewDocument.has_object_permission(self.context_mock, self.document))
        self.assertTrue(ViewDocument.has_object_permission(self.context_mock, self.user_document))

    def test_add_document(self) -> None:
        """Тестирование класса `AddDocument`."""
        self.assertFalse(AddDocument.has_object_permission(self.context_mock, self.period))
        with patch.object(self.user, 'has_perm', new=lambda perm: perm in ('dcis.view_project', 'dcis.view_period')):
            self.assertFalse(AddDocument.has_object_permission(self.context_mock, self.period))
        with patch.object(
            self.user,
            'has_perm',
            new=lambda perm: perm in ('dcis.view_project', 'dcis.view_period', 'dcis.add_document')
        ):
            self.assertTrue(AddDocument.has_object_permission(self.context_mock, self.period))
        self.assertFalse(AddDocument.has_object_permission(self.context_mock, self.user_period))
        for global_perm in ('dcis.add_project', 'dcis.add_period'):
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == global_perm):
                self.assertFalse(AddDocument.has_object_permission(self.context_mock, self.period))
                self.assertTrue(AddDocument.has_object_permission(self.context_mock, self.user_period))

    def test_change_document(self) -> None:
        """Тестирование класса `ChangeDocument`."""
        self._test_common(ChangeDocument, 'dcis.change_document', 'change_document')

    def test_delete_document(self) -> None:
        """Тестирование класса `DeleteDocument`."""
        self._test_common(DeleteDocument, 'dcis.delete_document', 'delete_document')

    def _test_common(self, cls: Type[BasePermission], permission: str, privilege: str) -> None:
        """Общий механизм тестирования для классов `ChangeDocument` и `DeleteDocument`."""
        self.assertFalse(cls.has_object_permission(self.context_mock, self.document))
        self.assertFalse(cls.has_object_permission(self.context_mock, self.user_document))
        with patch(
            'apps.dcis.permissions.document_permissions.ViewDocument.has_object_permission',
            new=Mock(return_value=True)
        ):
            self.assertFalse(cls.has_object_permission(self.context_mock, self.document))
            self.assertFalse(cls.has_object_permission(self.context_mock, self.user_document))
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == permission):
                self.assertTrue(cls.has_object_permission(self.context_mock, self.document))
                self.assertTrue(cls.has_object_permission(self.context_mock, self.user_document))
            for global_perm in ('dcis.add_project', 'dcis.add_period'):
                with patch.object(self.user, 'has_perm', new=lambda perm: perm == global_perm):
                    self.assertFalse(cls.has_object_permission(self.context_mock, self.document))
                    self.assertTrue(cls.has_object_permission(self.context_mock, self.user_document))
            with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
                self.assertTrue(cls.has_object_permission(self.context_mock, self.document))
                mock.assert_called_once_with(self.user.id, self.period.id, privilege)
            with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
                self.assertTrue(cls.has_object_permission(self.context_mock, self.user_document))
                mock.assert_called_once_with(self.user.id, self.user_period.id, privilege)
