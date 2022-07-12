"""Тесты вспомогательных функций для расчета значений ячеек."""

from django.test import TestCase


class CellHelpersTestCase(TestCase):
    """Тестирование вспомогательных функций для расчета ячеек."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        super().setUp()
        