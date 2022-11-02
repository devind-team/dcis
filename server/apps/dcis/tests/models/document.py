"""Тесты моделей документа."""
from datetime import timedelta

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Document, DocumentStatus, Period, Project, Status


class DocumentModelTestCase(TestCase):
    """Тестирование модели `Document`."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')

        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)

        self.status = Status.objects.create(name='Testing status')
        self.status_edit = Status.objects.create(edit=True)

        self.document_without_status_document = Document.objects.create(period=self.period)
        self.document_with_last_not_edit_status = Document.objects.create(period=self.period)
        self.document_statuses_with_last_not_edit_status = self._create_document_statuses(
            self.document_with_last_not_edit_status,
            [self.status, self.status_edit, self.status]
        )
        self.document_with_last_edit_status = Document.objects.create(period=self.period)
        self.document_statuses_with_last_edit_status = self._create_document_statuses(
            self.document_with_last_edit_status,
            [self.status, self.status, self.status_edit]
        )

    def test_last_status(self) -> None:
        """Тестирование свойства `last_status`."""
        self.assertIs(None, self.document_without_status_document.last_status)
        self.assertEqual(
            self.document_statuses_with_last_not_edit_status[2],
            self.document_with_last_not_edit_status.last_status
        )

    def test_is_editable(self) -> None:
        """Тестирование свойства `is_editable`."""
        self.assertFalse(self.document_without_status_document.is_editable)
        self.assertFalse(self.document_with_last_not_edit_status.is_editable)
        self.assertTrue(self.document_with_last_edit_status.is_editable)

    def _create_document_statuses(self, document: Document, statuses: list[Status]) -> list[DocumentStatus]:
        """Создание статусов документов."""
        document_statuses = [DocumentStatus(document=document, status=status, user=self.user) for status in statuses]
        document.documentstatus_set.bulk_create(document_statuses)
        for i, ds in enumerate(document_statuses):
            ds.created_at = ds.created_at + timedelta(days=i)
            ds.save(update_fields=('created_at',))
        return document_statuses
