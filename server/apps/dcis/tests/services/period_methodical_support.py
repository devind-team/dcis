from unittest import TestCase
from unittest.mock import patch

from devind_dictionaries.models import Organization
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied

from apps.core.models import User
from apps.dcis.models import CuratorGroup, Period, Project
from apps.dcis.permissions.period_permissions import can_change_period_methodical_support


class PeriodMethodicalSupportTestCase(TestCase):
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

    def test_add_period_methodical_support(self) -> None:
        """Тестирование функции добавления методических рекомендаций."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm not in ('can_change_period_methodical_support', 'change_period')
        ):
            self.assertRaises(PermissionDenied, can_change_period_methodical_support, self.superuser, self.period)
