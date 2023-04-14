from unittest.mock import patch

from devind_dictionaries.models import Organization
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.test import TransactionTestCase

from apps.core.models import User
from apps.dcis.models import CuratorGroup, Period, PeriodMethodicalSupport, Project
from apps.dcis.permissions.period_permissions import can_change_period_methodical_support
from apps.dcis.services.period_services import (
    add_period_methodical_support,
    change_period_methodical_support,
    delete_period_methodical_support,
)
from apps.dcis.tests.tests_helpers import create_in_memory_file


class PeriodMethodicalSupportTestCase(TransactionTestCase):
    """Тестирование методических рекомендаций."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)
        self.curator = User.objects.create(username='curator', email='curator@gmail.com')

        self.curator_group = CuratorGroup.objects.create(name='Кураторская группа')
        self.curator_group.users.add(self.curator)
        self.organization_content_type = ContentType.objects.get_for_model(Organization)
        self.project = Project.objects.create(content_type=self.organization_content_type)
        self.period = Period.objects.create(project=self.project)
        self.period_methodical_support = PeriodMethodicalSupport.objects.create(
            period=self.period,
            name='Methodical support name',
            src='storage/period_methodical_support/Me/Methodical support name'
        )
        self.file1 = create_in_memory_file('test_create_period.xlsx')
        self.file2 = create_in_memory_file('test_add_update_limitations_from_file.json')
        self.files = [self.file1, self.file2]

    def test_add_period_methodical_support(self) -> None:
        """Тестирование функции добавления методических рекомендаций."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, can_change_period_methodical_support, self.superuser, self.period)
        added_period_methodical_supports = add_period_methodical_support(
            files=self.files,
            period=self.period,
            user=self.superuser
        )
        expected_period_methodical_supports = PeriodMethodicalSupport.objects.filter(
            name__in=('test_create_period.xlsx', 'test_add_update_limitations_from_file.json')
        )
        self.assertEqual(
            [i for i in added_period_methodical_supports],
            [i for i in expected_period_methodical_supports]
        )

    def test_change_period_methodical_support(self) -> None:
        """Тестирование функции изменения методических рекомендаций."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, can_change_period_methodical_support, self.superuser, self.period)
        self.assertEqual(
            change_period_methodical_support(
                user=self.superuser,
                period=self.period,
                field='name',
                value='Changed name',
                file=self.period_methodical_support
            ),
            PeriodMethodicalSupport.objects.get(name='Changed name')
        )

    def test_delete_period_methodical_support(self) -> None:
        """Тестирование функции удаления методических рекомендаций."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(PermissionDenied, can_change_period_methodical_support, self.superuser, self.period)
        self.assertEqual(None, self._delete_period_methodical_support())
        self.assertQuerysetEqual(
            PeriodMethodicalSupport.objects.none(),
            PeriodMethodicalSupport.objects.filter(name='Methodical support')
        )

    def _delete_period_methodical_support(self) -> None:
        """Вызов функции `delete_period_methodical_support`."""
        return delete_period_methodical_support(
            user=self.superuser,
            period=self.period,
            file=self.period_methodical_support
        )
