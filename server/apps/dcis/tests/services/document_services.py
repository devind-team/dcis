"""Тестирование модуля, отвечающего за работу с документами."""
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department, Organization
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import CuratorGroup, Division, Document, Period, Project, RowDimension, Sheet, Status
from apps.dcis.permissions import (
    can_add_document,
    can_change_document_comment,
)
from apps.dcis.services.document_services import (
    change_document_comment,
    create_document,
    get_user_documents,
    get_user_roles,
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
        self.curator = User.objects.create(username='curator', email='curator@gmail.com')
        self.organization_member = User.objects.create(
            username='organization_member',
            email='organization_member@gmail.com',
        )
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.status = Status.objects.create(name='Testing status')

        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.department = Department.objects.create(user=self.superuser)

        self.organization_content_type = ContentType.objects.get_for_model(Organization)
        self.organization = Organization.objects.create(name=f'Организация', attributes='')
        self.organization.users.add(self.organization_member)

        self.curator_group = CuratorGroup.objects.create(name='Кураторская группа')
        self.curator_group.users.add(self.curator)
        self.curator_group.organization.add(self.organization)

        self.department_project = Project.objects.create(content_type=self.department_content_type)
        self.department_period = Period.objects.create(project=self.department_project)
        self.department_division = Division.objects.create(period=self.department_period, object_id=self.department.id)

        self.organization_project = Project.objects.create(content_type=self.organization_content_type)
        self.organization_period = Period.objects.create(project=self.organization_project)
        self.organization_multiple_period = Period.objects.create(project=self.organization_project, multiple=True)
        for period in [self.organization_period, self.organization_multiple_period]:
            Division.objects.create(period=period, object_id=self.organization.id)

        self.comment = 'Test comment'
        self.change_comment = 'Change comment'

        self.document = Document.objects.create(period=self.department_period)
        self.user_document = Document.objects.create(user=self.user, period=self.department_period)
        self.organization_document = Document.objects.create(period=self.organization_period)
        self.organization_multiple_document = Document.objects.create(
            period=self.organization_multiple_period,
            object_id=self.organization.id
        )

        self.superuser_document = Document.objects.create(
            user=self.superuser,
            period=self.department_period,
            comment=self.comment
        )

    def test_create_document(self) -> None:
        """Тестирование функции `create_document`."""
        with patch.object(self.superuser, 'has_perm', new=lambda perm: perm != 'dcis.add_document'):
            self.assertRaises(
                PermissionDenied,
                can_add_document,
                self.superuser,
                self.department_period,
                self.status,
                self.department_division.id
            )
        actual_document, _ = create_document(
            user=self.superuser,
            period=self.department_period,
            status=self.status,
            comment='Create document'
        )
        expected_document = Document.objects.get(comment='Create document')
        self.assertEqual(expected_document, actual_document)

    def test_get_user_roles(self) -> None:
        """Тестирование функции `get_user_roles`."""
        self.assertEqual([], get_user_roles(self.user, self.document))
        self.assertEqual(['creator'], get_user_roles(self.user, self.user_document))
        self.assertEqual([], get_user_roles(self.user, self.organization_multiple_document))
        self.assertEqual(['curator'], get_user_roles(self.curator, self.organization_multiple_document))
        self.assertEqual(['division_member'], get_user_roles(self.organization_member, self.organization_document))
        self.assertEqual(
            ['division_member'],
            get_user_roles(self.organization_member, self.organization_multiple_document)
        )

    def test_change_document_comment(self) -> None:
        """Тестирование функции `change_document_comment`."""
        with patch.object(self.superuser_document, 'user_id', new=None), patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm != 'dcis.change_document'
        ):
            self.assertRaises(PermissionDenied, can_change_document_comment, self.superuser, self.superuser_document)
        actual_document = change_document_comment(
            user=self.superuser,
            document=self.superuser_document,
            comment=self.change_comment
        )
        expected_document = Document.objects.get(comment=self.change_comment)
        self.assertEqual(expected_document, actual_document)
