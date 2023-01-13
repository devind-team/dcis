"""Тесты моделей документа."""
from datetime import timedelta

from devind_dictionaries.models import Organization
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Document, DocumentStatus, Period, Project, Status


class DocumentModelTestCase(TestCase):
    """Тестирование модели `Document`."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')

        self.organization_content_type = ContentType.objects.get_for_model(Organization)
        self.project = Project.objects.create(content_type=self.organization_content_type)
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


class DocumentStatusModelTestCase(TestCase):
    """Тестирование модели `DocumentStatus`."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')

        self.organization_content_type = ContentType.objects.get_for_model(Organization)
        self.project = Project.objects.create(content_type=self.organization_content_type)
        self.period = Period.objects.create(project=self.project)
        self.document = Document.objects.create(period=self.period)

        self.status = Status.objects.create()

    def test_create_save_delete(self) -> None:
        """Тестирование создания, обновления и удаления статуса документа."""
        document_status1 = DocumentStatus.objects.create(document=self.document, status=self.status, user=self.user)
        self.assertEqual(document_status1, self.document.last_status)
        document_status2 = self.document.documentstatus_set.create(
            document=self.document,
            status=self.status,
            user=self.user
        )
        self.assertEqual(document_status2, self.document.last_status)
        document_status2.created_at = document_status2.created_at - timedelta(days=1)
        document_status2.save(update_fields=('created_at',))
        self.assertEqual(document_status1, self.document.last_status)
        document_status1.delete()
        self.assertEqual(document_status2, self.document.last_status)
        document_status2.delete()
        self.assertIsNone(self.document.last_status)
