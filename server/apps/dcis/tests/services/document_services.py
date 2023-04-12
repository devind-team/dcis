"""Тестирование модуля, отвечающего за работу с документами."""

from unittest.mock import Mock, patch

from devind_dictionaries.models import Department, Organization
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import (
    AddStatus,
    CuratorGroup,
    Division,
    Document,
    DocumentMessage,
    Period,
    Project,
    RowDimension,
    Sheet,
    Status,
)
from apps.dcis.permissions import can_add_document
from apps.dcis.permissions.document_permissions import can_add_document_message
from apps.dcis.services.document_services import (
    create_document,
    create_document_message, get_user_documents,
    get_user_roles,
)


class GetUserDocumentsTestCase(TestCase):
    """Тестирование получения документов пользователя."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.organization_content_type = ContentType.objects.get_for_model(Organization)

        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.extra_user = User.objects.create(username='extra_user', email='extra_user@gmail.com')

        self.organizations = [Organization.objects.create(attributes='', user=self.user) for _ in range(3)]

        self.extra_project = Project.objects.create(content_type=self.organization_content_type)
        self.extra_period = Period.objects.create(project=self.extra_project)
        self.extra_row_document = Document.objects.create(period=self.extra_period)
        self.extra_organization_sheet = Sheet.objects.create(period=self.extra_period)
        self.extra_organization_row_dimensions = [RowDimension.objects.create(
            index=1,
            sheet=self.extra_organization_sheet,
            document=self.extra_row_document,
            object_id=organization.id
        ) for organization in self.organizations]

        self.user_is_creator_project = Project.objects.create(
            user=self.user,
            content_type=self.organization_content_type
        )
        self.user_is_not_creator_period = Period.objects.create(project=self.user_is_creator_project)
        self.user_is_creator_project_documents = [Document.objects.create(
            period=self.user_is_not_creator_period
        ) for _ in range(3)]

        self.user_is_not_creator_project = Project.objects.create(content_type=self.organization_content_type)
        self.user_is_creator_period = Period.objects.create(user=self.user, project=self.user_is_not_creator_project)
        self.user_is_creator_period_documents = [Document.objects.create(
            period=self.user_is_creator_period
        ) for _ in range(3)]

        self.multiple_single_project = Project.objects.create(content_type=self.organization_content_type)

        self.curator_organization = Organization.objects.create(attributes='')
        self.curator_group = CuratorGroup.objects.create()
        self.curator_group.users.add(self.user)
        self.curator_group.organization.add(self.curator_organization)

        self.multiple_period = Period.objects.create(project=self.multiple_single_project, multiple=True)
        self.multiple_period.division_set.create(object_id=self.curator_organization.id)
        self.multiple_period_user_document = Document.objects.create(period=self.multiple_period, user=self.user)
        self.multiple_period_curator_document = Document.objects.create(
            period=self.multiple_period,
            object_id=self.curator_organization.id,
        )
        self.organization_documents = [Document.objects.create(
            period=self.multiple_period, object_id=organization.id
        ) for organization in self.organizations]
        self.not_period_organization_documents = [Document.objects.create(
            period=self.extra_period, object_id=organization.id
        ) for organization in self.organizations]
        self.not_organization_document = Document.objects.create(period=self.multiple_period)

        self.single_not_curator_period, self.single_not_curator_documents = self._create_single_period()
        self.single_not_curator_extra_document = Document.objects.create(period=self.single_not_curator_period)

        self.single_curator_period, self.single_curator_documents = self._create_single_period()
        self.single_curator_extra_document = Document.objects.create(period=self.single_curator_period)
        self.single_curator_period.division_set.create(object_id=self.curator_organization.id)

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
                {
                    self.multiple_period_user_document,
                    self.multiple_period_curator_document,
                    *self.organization_documents
                },
                set(get_user_documents(self.user, period))
            )

    def test_get_user_documents_single_period_not_curator(self) -> None:
        """Тестирование функции `get_user_documents`.

        Для периода выбран единичный тип сбора, и пользователь не является куратором.
        """
        for period in self._get_period(self.single_not_curator_period):
            self.assertSetEqual(
                {*self.single_not_curator_documents},
                set(get_user_documents(self.user, period))
            )

    def test_get_user_documents_single_period_curator(self) -> None:
        """Тестирование функции `get_user_documents`.

        Для периода выбран единичный тип сбора, и пользователь является куратором.
        """
        for period in self._get_period(self.single_curator_period):
            self.assertSetEqual(
                {*self.single_curator_documents, self.single_curator_extra_document},
                set(get_user_documents(self.user, period))
            )

    def _create_single_period(self) -> tuple[Period, list[Document]]:
        """Создание периода с единичным типом сбора."""
        single_period = Period.objects.create(project=self.multiple_single_project, multiple=False)
        single_period_user_document = Document.objects.create(period=single_period, user=self.user)
        organization_row_document = Document.objects.create(period=single_period)
        organization_sheet = Sheet.objects.create(period=single_period)
        [RowDimension.objects.create(
            index=1,
            sheet=organization_sheet,
            document=organization_row_document,
            object_id=organization.id
        ) for organization in self.organizations]
        return single_period, [single_period_user_document, organization_row_document]

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
        self.add_status = AddStatus.objects.create(
            from_status=None,
            to_status=self.status,
            roles=['admin'],
        )

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

        self.document = Document.objects.create(period=self.department_period)
        self.user_document = Document.objects.create(user=self.user, period=self.department_period)
        self.organization_document = Document.objects.create(period=self.organization_period)
        self.organization_multiple_document = Document.objects.create(
            period=self.organization_multiple_period,
            object_id=self.organization.id
        )

        self.superuser_document = Document.objects.create(
            user=self.superuser,
            period=self.department_period
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
            status=self.status
        )
        expected_document = Document.objects.get(
            user=self.superuser,
            period=self.department_period,
            updated_by=self.superuser
        )
        self.assertEqual(expected_document, actual_document)
        self.assertEqual(self.status, actual_document.last_status.status)

    def test_get_user_roles(self) -> None:
        """Тестирование функции `get_user_roles`."""
        self.assertEqual(['admin', 'division_member'], get_user_roles(self.superuser, self.document))
        self.assertEqual([], get_user_roles(self.user, self.document))
        self.assertEqual(['creator'], get_user_roles(self.user, self.user_document))
        self.assertEqual([], get_user_roles(self.user, self.organization_multiple_document))
        self.assertEqual(['curator'], get_user_roles(self.curator, self.organization_multiple_document))
        self.assertEqual(['division_member'], get_user_roles(self.organization_member, self.organization_document))
        self.assertEqual(
            ['division_member'],
            get_user_roles(self.organization_member, self.organization_multiple_document)
        )


class DocumentMessageTestCase(TestCase):
    """Тестирование добавления сообщений к документу."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.curator = User.objects.create(username='curator', email='curator@gmail.com')
        self.another_curator = User.objects.create(username='another_curator', email='another_curator@gmail.com')
        self.organization_member = User.objects.create(
            username='organization_member',
            email='organization_member@gmail.com',
        )
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.organization_content_type = ContentType.objects.get_for_model(Organization)
        self.organization = Organization.objects.create(name=f'Организация', attributes='')
        self.organization.users.add(self.organization_member)

        self.curator_group = CuratorGroup.objects.create(name='Кураторская группа')
        self.curator_group.users.add(self.curator)
        self.curator_group.organization.add(self.organization)

        self.another_organization = Organization.objects.create(name=f'Другая организация', attributes='')
        self.another_organization.users.add(self.organization_member)
        self.another_curator_group = CuratorGroup.objects.create(name='Другая кураторская группа')
        self.another_curator_group.users.add(self.another_curator)

        self.organization_project = Project.objects.create(content_type=self.organization_content_type)
        self.organization_period = Period.objects.create(project=self.organization_project)

        self.user_document = Document.objects.create(
            user=self.user,
            period=self.organization_period,
            object_id=self.organization.id

        )
        self.superuser_document = Document.objects.create(
            user=self.superuser,
            period=self.organization_period
        )

    def test_create_document_user_and_superuser_message(self) -> None:
        """Тестирование функции create_document_message на добавление сообщения к документу посторонним пользователем
        и суперпользователем"""
        with patch.object(self.superuser_document, 'user_id', new=None), patch.object(
            self.superuser_document.period.project,
            'user_id',
            new=None
        ), patch.object(
            self.superuser_document.period,
            'user_id',
            new=None
        ), patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm not in ('dcis.change_document', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, can_add_document_message, self.superuser, self.superuser_document)
        actual_document_message = create_document_message(
            user=self.superuser,
            document=self.superuser_document,
            message='Test message',
            kind='message'
        )
        expected_document_message = DocumentMessage.objects.get(comment='Test message')
        self.assertEqual(expected_document_message, actual_document_message)
