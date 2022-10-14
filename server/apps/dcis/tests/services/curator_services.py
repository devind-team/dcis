"""Тесты модуля, отвечающего за работу кураторов."""

from django.test import TestCase

from apps.dcis.models import CuratorGroup
from apps.dcis.services.curator_services import add_curator_group


class CuratorGroupTestCase(TestCase):
    """Тестирование групп кураторов."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        pass

    def test_add_curator_group(self) -> None:
        """Тестирование функции `add_curator_group`."""
        curator_group: CuratorGroup = add_curator_group(name='test')
        self.assertEqual(
            CuratorGroup.objects.get(name='test'),
            curator_group,
        )
