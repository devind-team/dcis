"""Тестирование модуля, отвечающего за работу с документами."""
from datetime import timedelta
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Division, Document, DocumentStatus, Period, Project, RowDimension, Sheet, Status
from apps.dcis.permissions import (
    can_add_document,
    can_add_document_status,
    can_change_document,
    can_change_document_comment,
)
from apps.dcis.services.document_services import (
    add_document_status,
    change_document_comment,
    create_document,
    delete_document_status,
    get_user_documents,
)


class GetUserDocumentsTestCase(TestCase):
    """Тестирование получения документов пользователя."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.department_content_type = ContentType.objects.get_for_model(Department)

        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.extra_user = User.objects.create(username='extra_user', email='extra_user@gmail.com')

        self.departments = [Department.objects.create(user=self.user) for _ in range(3)]

        self.extra_project = Project.objects.create(content_type=self.department_content_type)
        self.extra_period = Period.objects.create(project=self.extra_project)
        self.extra_row_document = Document.objects.create(period=self.extra_period)
        self.extra_department_sheet = Sheet.objects.create(period=self.extra_period)
        self.extra_department_row_dimensions = [RowDimension.objects.create(
            index=1,
            sheet=self.extra_department_sheet,
            document=self.extra_row_document,
            object_id=department.id
        ) for department in self.departments]

        self.user_is_creator_project = Project.objects.create(
            user=self.user,
            content_type=self.department_content_type
        )
        self.user_is_not_creator_period = Period.objects.create(project=self.user_is_creator_project)
        self.user_is_creator_project_documents = [Document.objects.create(
            period=self.user_is_not_creator_period
        ) for _ in range(3)]

        self.user_is_not_creator_project = Project.objects.create(content_type=self.department_content_type)
        self.user_is_creator_period = Period.objects.create(user=self.user, project=self.user_is_not_creator_project)
        self.user_is_creator_period_documents = [Document.objects.create(
            period=self.user_is_creator_period
        ) for _ in range(3)]

        self.multiple_single_project = Project.objects.create(content_type=self.department_content_type)

        self.multiple_period = Period.objects.create(project=self.multiple_single_project, multiple=True)
        self.multiple_period_user_document = Document.objects.create(period=self.multiple_period, user=self.user)
        self.department_documents = [Document.objects.create(
            period=self.multiple_period, object_id=department.id
        ) for department in self.departments]
        self.not_period_department_documents = [Document.objects.create(
            period=self.extra_period, object_id=department.id
        ) for department in self.departments]
        self.not_department_document = Document.objects.create(period=self.multiple_period)

        self.single_period = Period.objects.create(project=self.multiple_single_project, multiple=False)
        self.single_period_user_document = Document.objects.create(period=self.single_period, user=self.user)
        self.department_row_document = Document.objects.create(period=self.single_period)
        self.department_sheet = Sheet.objects.create(period=self.single_period)
        self.department_row_dimensions = [RowDimension.objects.create(
            index=1,
            sheet=self.department_sheet,
            document=self.department_row_document,
            object_id=department.id
        ) for department in self.departments]
        self.not_department_row_document = Document.objects.create(period=self.single_period)

    def test_get_user_documents_with_global_perm(self) -> None:
        """Тестирование функции `get_user_documents`.

        Пользователь обладает глобальной привилегией `dcis.view_document`."""
        for period in self._get_period(self.user_is_not_creator_period):
            self.assertQuerysetEqual(
                self.user_is_not_creator_period.document_set.none(),
                get_user_documents(self.extra_user, period)
            )
            with patch.object(self.extra_user, 'has_perm', new=Mock(return_value=True)) as mock:
                documents = get_user_documents(self.extra_user, period)
                mock.assert_called_once_with('dcis.view_document')
                self.assertQuerysetEqual(self.user_is_not_creator_period.document_set.all(), documents)

    def test_get_user_documents_with_local_perm(self) -> None:
        """Тестирование функции `get_user_documents`.

        Пользователь обладает локальной привилегией `view_document`."""
        for period in self._get_period(self.user_is_creator_period):
            self.assertQuerysetEqual(
                self.user_is_creator_period.document_set.none(),
                get_user_documents(self.extra_user, period)
            )
            with patch('apps.dcis.services.document_services.has_privilege', new=Mock(return_value=True)) as mock:
                documents = get_user_documents(self.extra_user, period)
                mock.assert_called_once_with(self.extra_user.id, self.user_is_creator_period.id, 'view_document')
                self.assertQuerysetEqual(self.user_is_creator_period.document_set.all(), documents)

    def test_get_user_documents_user_is_project_creator(self) -> None:
        """Тестирование функции `get_user_documents`.

        Пользователь является создателем проекта периода.
        """
        for period in self._get_period(self.user_is_not_creator_period):
            self.assertQuerysetEqual(
                self.user_is_not_creator_period.document_set.all(),
                get_user_documents(self.user, period)
            )

    def test_get_user_documents_user_is_period_creator(self) -> None:
        """Тестирование функции `get_user_documents`.

        Пользователь является создателем периода.
        """
        for period in self._get_period(self.user_is_creator_period):
            self.assertQuerysetEqual(
                self.user_is_creator_period.document_set.all(),
                get_user_documents(self.user, period)
            )

    def test_get_user_documents_multiple_period(self) -> None:
        """Тестирование функции `get_user_documents`.

        Для периода выбран множественный тип сбора.
        """
        for period in self._get_period(self.multiple_period):
            self.assertSetEqual(
                {self.multiple_period_user_document, *self.department_documents},
                set(get_user_documents(self.user, period))
            )

    def test_get_user_documents_single_period(self) -> None:
        """Тестирование функции `get_user_documents`.

        Для периода выбран единичный тип сбора.
        """
        for period in self._get_period(self.single_period):
            self.assertSetEqual(
                {self.single_period_user_document, self.department_row_document},
                set(get_user_documents(self.user, period))
            )

    @staticmethod
    def _get_period(period: Period):
        """Получение периода и идентификаторов периода в виде int и str."""
        yield period
        yield period.id
        yield str(period.id)


class DocumentTestCase(TestCase):
    """Тестирование разных функций работы с документом."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.super_user = User.objects.create(username='super_user', email='super_user@gmain.com', is_superuser=True)

        self.status = Status.objects.create(name='Testing status')
        self.status_str = Status.objects.create(name='Test status')
        self.status_edit = Status.objects.create(edit=True)

        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.department = Department.objects.create(user=self.super_user)
        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)
        self.department_division = Division.objects.create(period=self.period, object_id=self.department.id)

        self.comment = 'Test comment'
        self.change_comment = 'Change comment'
        self.document = Document.objects.create(
            user=self.super_user,
            period=self.period,
            comment=self.comment
        )
        self.document_status = DocumentStatus.objects.create(
            user=self.super_user,
            document=self.document,
            status=self.status,
            comment=self.comment
        )

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

    def test_create_document(self) -> None:
        """Тестирование функции `create_document`."""
        with patch.object(self.super_user, 'has_perm', new=lambda perm: perm != 'dcis.add_document'):
            self.assertRaises(
                PermissionDenied,
                can_add_document,
                self.super_user,
                self.period,
                self.status,
                self.department_division.id
            )
        document = create_document(user=self.super_user,
                                   period=self.period,
                                   status=self.status,
                                   comment='Create document')[0]
        self.assertEqual(
            document,
            Document.objects.get(comment='Create document'),
            'Create document'
        )

    def test_add_document_status(self) -> None:
        """Тестирование функции `add_document_status`."""
        with patch.object(self.super_user, 'has_perm', new=lambda perm: perm != 'dcis.change_document'):
            self.assertRaises(PermissionDenied, can_add_document_status, self.super_user, self.document, self.status)
        self.assertEqual(
            add_document_status(
                user=self.super_user,
                document=self.document,
                status=self.status_str,
                comment='Add document status'
            ),
            DocumentStatus.objects.get(comment='Add document status'),
            'Add document status'
        )

    def test_change_document_comment(self) -> None:
        """Тестирование функции `change_document_comment`."""
        with patch.object(self.document, 'user_id', new=None), patch.object(
            self.super_user,
            'has_perm',
            new=lambda perm: perm != 'dcis.change_document'
        ):
            self.assertRaises(PermissionDenied, can_change_document_comment, self.super_user, self.document)
        self.assertEqual(
            change_document_comment(user=self.super_user, document=self.document, comment=self.change_comment),
            Document.objects.get(comment=self.change_comment),
            'Change document comment'
        )

    def test_delete_document_status(self) -> None:
        """Тестирование функции `delete_document_status`."""
        with patch.object(self.super_user, 'has_perm', new=lambda perm: perm != 'dcis.change_document'):
            self.assertRaises(PermissionDenied, can_change_document, self.super_user, self.document)
        self.assertEqual(
            delete_document_status(user=self.super_user, status=self.document_status),
            None,
            'Delete document status'
        )
