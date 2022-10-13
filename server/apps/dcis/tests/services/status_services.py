from unittest.mock import patch

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Document, DocumentStatus, Period, Project, Status
from apps.dcis.permissions import (
    can_add_document_status,
    can_change_document,
)
from apps.dcis.services.status_services import add_document_status, delete_document_status


class StatusTestCase(TestCase):
    """Тестирование разных функций работы со статусами."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.status = Status.objects.create(name='Testing status')
        self.status_str = Status.objects.create(name='Test status')

        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)

        self.comment = 'Test comment'
        self.document = Document.objects.create(
            period=self.period,
            comment=self.comment
        )
        self.superuser_document = Document.objects.create(
            user=self.superuser,
            period=self.period,
            comment=self.comment
        )
        self.document_status = DocumentStatus.objects.create(
            user=self.superuser,
            document=self.document,
            status=self.status,
            comment=self.comment
        )

    def test_add_document_status(self) -> None:
        """Тестирование функции `add_document_status`."""
        with patch.object(self.superuser, 'has_perm', new=lambda perm: perm != 'dcis.change_document'):
            self.assertRaises(PermissionDenied, can_add_document_status, self.superuser, self.document, self.status)
        document_status = add_document_status(
            user=self.superuser,
            document=self.superuser_document,
            status=self.status_str,
            comment='Add document status'
        )
        self.assertEqual(
            DocumentStatus.objects.get(comment='Add document status'),
            document_status
        )

    def test_delete_document_status(self) -> None:
        """Тестирование функции `delete_document_status`."""
        with patch.object(self.superuser, 'has_perm', new=lambda perm: perm != 'dcis.change_document'):
            self.assertRaises(PermissionDenied, can_change_document, self.superuser, self.superuser_document)
        self.assertEqual(
            None,
            delete_document_status(user=self.superuser, status=self.document_status),
        )
