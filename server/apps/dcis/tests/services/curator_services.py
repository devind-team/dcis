"""Тесты модуля, отвечающего за работу кураторов."""

from unittest.mock import patch

from devind_dictionaries.models import Department, Organization
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import CuratorGroup, Document, Period, Project
from apps.dcis.services.curator_services import (
    add_curator_group,
    add_organization_curator_group,
    add_users_curator_group,
    delete_curator_group,
    delete_organization_curator_group,
    delete_user_curator_group,
    get_curator_groups,
    get_curator_organizations,
    is_document_curator,
    is_period_curator,
)


class CuratorGroupTestCase(TestCase):
    """Тестирование групп кураторов."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)
        self.group_user = User.objects.create(username='group_user', email='group_user@gmail.com')

        self.curator_groups = [CuratorGroup.objects.create(name=f'Кураторская группа №{i}') for i in range(3)]
        self.extra_curator_groups = CuratorGroup.objects.create(name='Кураторская группа №3')
        self.organizations = [Organization.objects.create(name=f'Организация №{i}', attributes='') for i in range(3)]
        for curator_group, organization in zip(self.curator_groups, self.organizations):
            curator_group.users.add(self.group_user)
            curator_group.organization.add(organization)

        self.department_project = Project.objects.create(content_type=ContentType.objects.get_for_model(Department))
        self.department_period = Period.objects.create(project=self.department_project)
        self.department_document = Document.objects.create(period=self.department_period)

        self.organization_project = Project.objects.create(content_type=ContentType.objects.get_for_model(Organization))

        self.organization_multiple_period = Period.objects.create(multiple=True, project=self.organization_project)
        self.organization_multiple_document = Document.objects.create(period=self.organization_multiple_period)
        self.organization_multiple_user_document = Document.objects.create(
            period=self.organization_multiple_period,
            object_id=self.organizations[0].id
        )

        self.organization_period = Period.objects.create(project=self.organization_project)
        self.organization_document = Document.objects.create(period=self.organization_period)
        self.organization_period.division_set.create(object_id=self.organizations[0].id)

        self.curator_group = CuratorGroup.objects.create(name='cur')
        self.organization = Organization.objects.create(
            name='name',
            present_name='pres name',
            attributes=''
        )
        self.group = Group.objects.create(name='group')

        self.curator_group_2 = CuratorGroup.objects.create(name='cur_1')
        self.organization_2 = Organization.objects.create(
            name='name_1',
            present_name='pres name_1',
            attributes=''
        )
        self.curator_group_2.users.add(self.superuser)
        self.curator_group_2.organization.add(self.organization)

    def test_get_curator_groups(self) -> None:
        """Тестирование функции `get_curator_groups`."""
        self.assertEqual(self.curator_groups, list(get_curator_groups(self.group_user)))
        self.assertEqual([], list(get_curator_groups(self.user)))

    def test_get_curator_organizations(self) -> None:
        """Тестирование функции `get_curator_organizations`."""
        self.assertEqual(self.organizations, list(get_curator_organizations(self.group_user)))
        self.assertEqual([], list(get_curator_organizations(self.user)))

    def test_is_period_curator(self) -> None:
        """Тестирование функции `is_period_curator`."""
        self.assertFalse(is_period_curator(self.group_user, self.department_period))
        self.assertFalse(is_period_curator(self.user, self.department_period))
        self.assertTrue(is_period_curator(self.group_user, self.organization_period))
        self.assertFalse(is_period_curator(self.user, self.organization_period))

    def test_is_document_curator(self) -> None:
        """Тестирование функции `is_document_curator`."""
        self.assertFalse(is_document_curator(self.group_user, self.department_document))
        self.assertFalse(is_document_curator(self.user, self.organization_multiple_document))
        self.assertFalse(is_document_curator(self.group_user, self.organization_multiple_document))
        self.assertFalse(is_document_curator(self.user, self.organization_multiple_user_document))
        self.assertTrue(is_document_curator(self.group_user, self.organization_multiple_user_document))
        self.assertFalse(is_document_curator(self.user, self.organization_document))
        self.assertTrue(is_document_curator(self.group_user, self.organization_document))

    def test_add_curator_group(self) -> None:
        """Тестирование функции `add_curator_group`."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm != 'dcis.add_curatorgroup'
        ), self.assertRaises(PermissionDenied):
            add_curator_group(user=self.superuser, name='test', group_id=self.group.id)
        curator_group = add_curator_group(user=self.superuser, name='test', group_id=self.group.id)
        self.assertEqual(
            CuratorGroup.objects.get(name='test'),
            curator_group,
        )

    def test_delete_curator_group(self) -> None:
        """Тестирование функции `delete_curator_group`."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm != 'dcis.delete_curatorgroup'
        ), self.assertRaises(PermissionDenied):
            delete_curator_group(user=self.superuser, curator_group_id=self.curator_group.id)
        self.assertEqual(
            None,
            delete_curator_group(user=self.superuser, curator_group_id=self.curator_group.id)
        )

    def test_add_users_curator_group(self) -> None:
        """Тестирование функции `add_users_curator_group`."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm != 'dcis.change_curatorgroup'
        ), self.assertRaises(PermissionDenied):
            add_users_curator_group(
                user=self.superuser,
                curator_group_id=self.curator_group.id,
                user_ids=[self.user.id, self.superuser.id]
            )
        user_curator_group = add_users_curator_group(
            user=self.superuser,
            curator_group_id=self.curator_group.id,
            user_ids=[self.user.id, self.superuser.id]
        )
        self.assertEqual(
            {self.user, self.superuser},
            set(user_curator_group),
        )

    def test_delete_user_curator_group(self) -> None:
        """Тестирование функции `delete_user_curator_group`."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm != 'dcis.change_curatorgroup'
        ), self.assertRaises(PermissionDenied):
            delete_user_curator_group(
                user=self.superuser,
                curator_group_id=self.curator_group_2.id,
                user_id=self.superuser.id
            )
        self.assertEqual(
            None,
            delete_user_curator_group(
                user=self.superuser,
                curator_group_id=self.curator_group_2.id,
                user_id=self.superuser.id
            )
        )

    def test_add_organizations_curator_group(self) -> None:
        """Тестирование функции `add_organizations_curator_group`."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm != 'dcis.change_curatorgroup'
        ), self.assertRaises(PermissionDenied):
            add_organization_curator_group(
                user=self.superuser,
                curator_group_id=self.curator_group.id,
                organization_ids=[self.organization.id, self.organization_2.id]
            )
        organization_curator_group = add_organization_curator_group(
            user=self.superuser,
            curator_group_id=self.curator_group.id,
            organization_ids=[self.organization.id, self.organization_2.id]
        )
        self.assertEqual(
            {self.organization, self.organization_2},
            set(organization_curator_group),
        )

    def test_delete_organization_curator_group(self) -> None:
        """Тестирование функции `delete_organization_curator_group`."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm != 'dcis.change_curatorgroup'
        ), self.assertRaises(PermissionDenied):
            delete_organization_curator_group(
                user=self.superuser,
                curator_group_id=self.curator_group_2.id,
                organization_id=self.organization_2.id
            )
        self.assertEqual(
            None,
            delete_organization_curator_group(
                user=self.superuser,
                curator_group_id=self.curator_group_2.id,
                organization_id=self.organization_2.id
            )
        )
