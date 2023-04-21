from django.test import TestCase

from apps.dcis.services.formula_services import translate_formula_en2ru, translate_formula_ru2en


class FormulaServicesTestCase(TestCase):
    """Тест обработки формул."""

    def test_translate_formula_en2ru(self) -> None:
        self.assertEqual(
            translate_formula_en2ru("SUMIFS('Форма 1'!C7:C8)>=SUM('Форма 1а'!C7:C8)"),
            "СУММЕСЛИМН('Форма 1'!C7:C8)>=СУММ('Форма 1а'!C7:C8)"
        ),
        self.assertEqual(translate_formula_en2ru("SUM(1.3,2.5)"), "СУММ(1,3;2,5)"),
        self.assertEqual(translate_formula_en2ru('LOWER("F,F")'), 'СТРОЧН("F,F")')

    def test_translate_formula_ru2en(self) -> None:
        self.assertEqual(
            translate_formula_ru2en("СУММЕСЛИМН('Форма 1'!C7:C8)>=СУММ('Форма 1а'!C7:C8)"),
            "SUMIFS('Форма 1'!C7:C8)>=SUM('Форма 1а'!C7:C8)"
        ),
        self.assertEqual(translate_formula_ru2en("СУММ(1,3;2,5)"), "SUM(1.3,2.5)"),
        self.assertEqual(translate_formula_ru2en('СТРОЧН("F,F")'), 'LOWER("F,F")')
