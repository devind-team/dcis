"""Тесты модуля, отвечающего за работу с привилегиями."""

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Period, PeriodGroup, PeriodPrivilege, Privilege, Project
from apps.dcis.services.privilege_services import has_group_privilege, has_individual_privilege, has_privilege


class PrivilegeTestCase(TestCase):
    """Тесты модуля, отвечающего за работу с привилегиями."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.project = Project.objects.create(content_type=ContentType.objects.get_for_model(Department))
        self.period = Period.objects.create(project=self.project)

        self.individual_privilege = Privilege.objects.create(key='individual_privilege')
        self.period_privilege = PeriodPrivilege.objects.create(
            period=self.period,
            user=self.user,
            privilege=self.individual_privilege
        )

        self.group_privilege = Privilege.objects.create(key='group_privilege')
        self.period_group = PeriodGroup.objects.create(period=self.period)
        self.period_group.users.add(self.user)
        self.period_group.privileges.add(self.group_privilege)

    def test_has_individual_privilege(self) -> None:
        """Тестирование функции `has_individual_privilege`."""
        self.assertTrue(has_individual_privilege(self.user.id, self.period.id, 'individual_privilege'))
        self.assertFalse(has_individual_privilege(self.user.id, self.period.id, 'group_privilege'))

    def test_has_group_privilege(self) -> None:
        """Тестирование функции `has_group_privilege`."""
        self.assertTrue(has_group_privilege(self.user.id, self.period.id, 'group_privilege'))
        self.assertFalse(has_group_privilege(self.user.id, self.period.id, 'individual_privilege'))

    def test_has_privilege(self) -> None:
        """Тестирование функции `has_privilege`"""
        self.assertTrue(has_privilege(self.user.id, self.period.id, 'individual_privilege'))
        self.assertTrue(has_privilege(self.user.id, self.period.id, 'group_privilege'))
        self.assertFalse(has_privilege(self.user.id, self.period.id, 'wrong_privilege'))
