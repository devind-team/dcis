from unittest import TestCase

from apps.dcis.services.formula_services import translate_formula_en2ru, translate_formula_ru2en


class FormulaServicesTestCase(TestCase):
    """Тест обработки формул."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.formula_en = "SUMIFS('Форма 1'!C7:C8)>=SUM('Форма 1а'!C7:C8)"
        self.formula_ru = "СУММЕСЛИМН('Форма 1'!C7:C8)>=СУММ('Форма 1а'!C7:C8)"


    def test_translate_formula_en2ru(self) -> None:
        self.assertEqual(translate_formula_en2ru(self.formula_en), self.formula_ru)

    def test_translate_formula_ru2en(self) -> None:
        self.assertEqual(translate_formula_ru2en(self.formula_ru), self.formula_en)
