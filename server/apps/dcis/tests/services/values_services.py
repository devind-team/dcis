"""Тестирование сервисов для действий со значениями."""

from django.test import TestCase


class ValueServicesTestCase(TestCase):
    """Тестирование сервисов для работы с действиями."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        super().setUp()
