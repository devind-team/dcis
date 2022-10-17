"""Тесты модуля, отвечающего за работу со статусами."""
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import AddStatus, Document, DocumentStatus, Period, Project, Status
from apps.dcis.services.status_services import add_document_status, delete_document_status


class StatusTestCase(TestCase):
    """Тестирование разных функций работы со статусами."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)

        self.status_to_add = Status.objects.create(name='add_status')
        self.exist_status = Status.objects.create(name='exist_status')
        self.add_status = AddStatus.objects.create(
            from_status=self.exist_status,
            to_status=self.status_to_add,
            roles=[],
            check='test_check',
        )
        self.add_document = Document.objects.create(user=self.superuser, period=self.period)
        self.add_document_status = DocumentStatus.objects.create(
            user=self.superuser,
            document=self.add_document,
            status=self.exist_status,
        )

        self.status_to_delete = Status.objects.create(name='delete_status')
        self.delete_document = Document.objects.create(period=self.period)
        self.delete_document_status = DocumentStatus.objects.create(
            user=self.superuser,
            document=self.delete_document,
            status=self.status_to_delete,
        )

    def test_add_document_status(self) -> None:
        """Тестирование функции `add_document_status`."""
        with patch.object(
            self.superuser, 'has_perm', new=lambda perm: perm != 'dcis.change_document'
        ), self.assertRaises(PermissionDenied):
            self._add_document_status()
        with patch(
            'apps.dcis.services.status_services.StatusCheck.test_check',
            create=True,
            new=Mock()
        ) as mock:
            actual_document_status = self._add_document_status()
            mock.assert_called_once_with(self.add_document)
        expected_document_status = DocumentStatus.objects.get(comment='Add document status')
        self.assertEqual(expected_document_status, actual_document_status)

    def test_delete_document_status(self) -> None:
        """Тестирование функции `delete_document_status`."""
        with patch.object(
            self.superuser, 'has_perm', new=lambda perm: perm != 'dcis.change_document'
        ), self.assertRaises(PermissionDenied):
            self._delete_document_status()
        self.assertIsNone(delete_document_status(user=self.superuser, status=self.delete_document_status))

    def _add_document_status(self) -> DocumentStatus:
        """Добавление статуса документа."""
        return add_document_status(
            user=self.superuser,
            document=self.add_document,
            status=self.status_to_add,
            comment='Add document status'
        )

    def _delete_document_status(self) -> None:
         """Удаление статуса документа."""
         delete_document_status(user=self.superuser, status=self.delete_document_status)
