"""Тесты модуля, отвечающего за работу кураторов."""

from devind_dictionaries.models import Organization
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

        self.user: User = User.objects.create(username='user', email='user@gmain.com')
        self.curator_group: CuratorGroup = CuratorGroup.objects.create(name="cur")
        self.organization: Organization = Organization.objects.create(
            name='name',
            present_name='pres name',
            attributes=''
        )

        self.curator_group_2: CuratorGroup = CuratorGroup.objects.create(name="cur_1")
        self.organization_2: Organization = Organization.objects.create(
            name='name_1',
            present_name='pres name_1',
            attributes=''
        )
        self.curator_group_2.users.add(self.user)
        self.curator_group_2.organization.add(self.user)

    def test_add_curator_group(self) -> None:
        """Тестирование функции `add_curator_group`."""
        curator_group: CuratorGroup = add_curator_group(name='test')
        self.assertEqual(
            CuratorGroup.objects.get(name='test'),
            curator_group,
        )

    def test_delete_curator_group(self) -> None:
        """Тестирование функции `delete_curator_group`."""
        self.assertEqual(
            None,
            delete_curator_group(curator_group_id=self.curator_group.id)
        )

    def test_add_user_curator_group(self) -> None:
        """Тестирование функции `add_user_curator_group`."""
        user_curator_group: str | int = add_user_curator_group(
            curator_group_id=self.curator_group.id,
            user_id=self.user.id
        )
        self.assertEqual(
            self.user.id,
            user_curator_group,
        )

    def test_delete_user_curator_group(self) -> None:
        """Тестирование функции `delete_user_curator_group`."""
        self.assertEqual(
            None,
            delete_user_curator_group(curator_group_id=self.curator_group_2.id, user_id=self.user.id)
        )

    def test_add_organization_curator_group(self) -> None:
        """Тестирование функции `add_organization_curator_group`."""
        organization_curator_group: str | int = add_organization_curator_group(
            curator_group_id=self.curator_group.id,
            organization_id=self.organization.id
        )
        self.assertEqual(
            self.organization.id,
            organization_curator_group,
        )

    def test_delete_organization_curator_group(self) -> None:
        """Тестирование функции `delete_organization_curator_group`."""
        self.assertEqual(
            None,
            delete_organization_curator_group(
                curator_group_id=self.curator_group_2.id,
                organization_id=self.organization_2.id
            )
        )
