"""Тестирование модуля, отвечающего за работу с документами."""

from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Document, Period, Project, RowDimension, Sheet
from apps.dcis.services.document_services import get_user_documents


class GetUserDocumentsTestCase(TestCase):
    """Тестирование получения документов пользователя."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.department_content_type = ContentType.objects.get_for_model(Department)

        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.extra_user = User.objects.create(username='extra_user', email='extra_user@gmail.com')

        self.departments = [Department.objects.create(user=self.user) for _ in range(3)]

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
        self.department_documents = [Document.objects.create(
            period=self.multiple_period, object_id=department.id
        ) for department in self.departments]
        self.not_department_document = Document.objects.create(period=self.multiple_period)

        self.single_period = Period.objects.create(project=self.multiple_single_project, multiple=False)
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
                set(self.department_documents),
                set(get_user_documents(self.user, period))
            )

    def test_get_user_documents_single_period(self) -> None:
        """Тестирование функции `get_user_documents`.

        Для периода выбран единичный тип сбора.
        """
        for period in self._get_period(self.single_period):
            self.assertSetEqual(
                {self.department_row_document},
                set(get_user_documents(self.user, period))
            )

    @staticmethod
    def _get_period(period: Period):
        """Получение периода и идентификаторов периода в виде int и str."""
        yield period
        yield period.id
        yield str(period.id)
