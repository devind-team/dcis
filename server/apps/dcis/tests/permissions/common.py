"""Общая логика для тестирования разрешений."""

from unittest.mock import Mock

from django.test import TestCase

from apps.core.models import User


class PermissionsTestCase(TestCase):
    """Общие данные для тестирования разрешений."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.context_mock = Mock()
        self.context_mock.user = self.user
