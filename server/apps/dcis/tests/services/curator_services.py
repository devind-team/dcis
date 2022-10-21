"""Тесты модуля, отвечающего за работу кураторов."""
from unittest.mock import patch

from devind_dictionaries.models import Organization
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import CuratorGroup
from apps.dcis.services.curator_services import (
    add_curator_group,
    add_organization_curator_group, add_user_curator_group,
    delete_curator_group,
    delete_organization_curator_group, delete_user_curator_group,
)


class CuratorGroupTestCase(TestCase):
    """Тестирование групп кураторов."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""

        self.superuser = User.objects.create(username='user', email='superuser@gmain.com', is_superuser=True)
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

    def test_add_user_curator_group(self) -> None:
        """Тестирование функции `add_user_curator_group`."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm != 'dcis.change_curatorgroup'
        ), self.assertRaises(PermissionDenied):
            add_user_curator_group(
                user=self.superuser,
                curator_group_id=self.curator_group.id,
                user_id=self.superuser.id
            )
        user_curator_group = add_user_curator_group(
            user=self.superuser,
            curator_group_id=self.curator_group.id,
            user_id=self.superuser.id
        )
        self.assertEqual(
            self.superuser.id,
            user_curator_group,
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

    def test_add_organization_curator_group(self) -> None:
        """Тестирование функции `add_organization_curator_group`."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm != 'dcis.change_curatorgroup'
        ), self.assertRaises(PermissionDenied):
            add_organization_curator_group(
                user=self.superuser,
                curator_group_id=self.curator_group.id,
                organization_id=self.organization.id
            )
        organization_curator_group = add_organization_curator_group(
            user=self.superuser,
            curator_group_id=self.curator_group.id,
            organization_id=self.organization.id
        )
        self.assertEqual(
            self.organization.id,
            organization_curator_group,
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
