"""Тестирование вспомогательного модуля для расчета формул."""

from django.test import TestCase
from xlsx_evaluate import Evaluator, ModelCompiler

from apps.dcis.helpers.cell import evaluate_formula


class CellHelpersTestCase(TestCase):
    """Тестирование вспомогательного модуля для расчета формул."""

    def test_evaluate_formula(self) -> None:
        """Тестирование функции `evaluate_formula`."""
        compiler = ModelCompiler()
        model = compiler.read_and_parse_dict(input_dict={
            'A1': 2,
            'A2': '=A1 / 0',
            'A3': '=A1 + A3',
            'A4': '=A1 + 2',
        }, default_sheet='sheet1')
        evaluator = Evaluator(model)
        self.assertEqual((False, 'Деление на 0'), evaluate_formula(evaluator, 'sheet1!A2'))
        self.assertEqual((False, 'Циклическая ссылка'), evaluate_formula(evaluator, 'sheet1!A3'))
        self.assertEqual((True, '4'), evaluate_formula(evaluator, 'sheet1!A4'))
