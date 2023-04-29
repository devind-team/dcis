"""Тесты модуля, отвечающего за работу с листами."""

from typing import Iterable
from unittest.mock import patch

from devind_dictionaries.models import Organization
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings

from apps.core.models import User
from apps.dcis.helpers.sheet_formula_cache import SheetFormulaContainerCache
from apps.dcis.models import Cell, ColumnDimension, Document, Period, Project, RowDimension, Sheet
from apps.dcis.models.sheet import KindCell, Style, Value
from apps.dcis.services.sheet_services import (
    CellPasteOptions,
    CellPasteStyle,
    CheckCellOptions,
    change_cell_formula,
    paste_into_cells,
)
from apps.dcis.services.value_services import ValueInput, update_or_create_values
from apps.dcis.tasks import recalculate_cell_task


class CheckCellOptionsTestCase(TestCase):
    """Тестирование класса `CheckCellOptions`."""

    def test_not_allowed_field(self) -> None:
        """Тестирование неразрешенного поля."""
        result = CheckCellOptions('field', 'value')
        self.assertIsInstance(result, CheckCellOptions.Error)
        self.assertEqual('field', result.field)
        self.assertIn('не в списке', result.error)

    def test_standard(self) -> None:
        """Тестирование стандартной проверки."""
        allowed_map = {
            'horizontal_align': CheckCellOptions._allowed_horizontal_align,
            'vertical_align': CheckCellOptions._allowed_vertical_align,
            'underline': CheckCellOptions._allowed_underline,
            'kind': CheckCellOptions._allowed_kinds,
            'aggregation': CheckCellOptions._allow_aggregation,
        }
        for field, allowed_values in allowed_map.items():
            for allowed_value in allowed_values:
                result = CheckCellOptions(field, allowed_value)
                self.assertIsInstance(result, CheckCellOptions.Success)
                self.assertEqual(allowed_value, result.value)
            result = CheckCellOptions(field, 'value')
            self.assertIsInstance(result, CheckCellOptions.Error)
            self.assertEqual(field, result.field)
            self.assertIn('не в списке', result.error)

    def test_size(self) -> None:
        """Тестирование поля `size`."""
        result = CheckCellOptions('size', 'str')
        self.assertIsInstance(result, CheckCellOptions.Error)
        self.assertEqual('size', result.field)
        self.assertIn('не является числом', result.error)
        for out_value in ['5', '37']:
            result = CheckCellOptions('size', out_value)
            self.assertIsInstance(result, CheckCellOptions.Error)
            self.assertEqual('size', result.field)
            self.assertIn(f'6 <= {out_value} <= 36', result.error)
        for in_value in [6, 16, 36]:
            result = CheckCellOptions('size', str(in_value))
            self.assertIsInstance(result, CheckCellOptions.Success)
            self.assertEqual(in_value, result.value)

    def test_bool(self) -> None:
        """Тестирование полей типа `bool`."""
        for field in ['strong', 'italic', 'strike', 'editable']:
            result = CheckCellOptions(field, 'value')
            self.assertIsInstance(result, CheckCellOptions.Error)
            self.assertEqual(field, result.field)
            self.assertIn('не в списке', result.error)
            for value in [True, False]:
                result = CheckCellOptions(field, str(value).lower())
                self.assertIsInstance(result, CheckCellOptions.Success)
                self.assertEqual(value, result.value)


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
@patch(
    'apps.dcis.services.sheet_services.recalculate_cell_task.delay',
    new=lambda *args: recalculate_cell_task.apply(args=args),
)
class ChangeCellFormulaTestCase(TestCase):
    """Тестирование функции `change_cell_formula`."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.organization_content_type = ContentType.objects.get_for_model(Organization)
        self.project = Project.objects.create(content_type=self.organization_content_type)
        self.period = Period.objects.create(project=self.project)

        self.form1 = Sheet.objects.create(name='Форма №1', period=self.period)
        self.form1_row = RowDimension.objects.create(index=1, sheet=self.form1)
        self.form1_columns = [ColumnDimension.objects.create(index=i, sheet=self.form1) for i in range(1, 4)]
        self.form1_cache_container = SheetFormulaContainerCache(name=self.form1.name)
        self.form1_cells: list[Cell] = []
        for i, column in enumerate(self.form1_columns, 1):
            if i == 1:
                formula = "=SUM(B1:C1) + SUM('Форма №2'!A1:C1)"
                self.form1_cells.append(Cell.objects.create(
                    kind=KindCell.NUMERIC,
                    formula=formula,
                    default=f'11.0',
                    column=column,
                    row=self.form1_row,
                ))
                self.form1_cache_container.add_formula('A1', formula)
            else:
                self.form1_cells.append(Cell.objects.create(
                    kind=KindCell.NUMERIC,
                    default=f'{i:.1f}',
                    column=column,
                    row=self.form1_row,
                ))
        self.form1_cache_container.save(sheet_id=self.form1.id)

        self.form2 = Sheet.objects.create(name='Форма №2', period=self.period)
        self.form2_row = RowDimension.objects.create(index=1, sheet=self.form2)
        self.form2_columns = [ColumnDimension.objects.create(index=i, sheet=self.form2) for i in range(1, 4)]
        self.form2_cells: list[Cell] = []
        for i, column in enumerate(self.form2_columns):
            self.form2_cells.append(Cell.objects.create(
                kind=KindCell.NUMERIC,
                default=f'{i:.1f}',
                column=column,
                row=self.form2_row,
            ))

        self.organization = Organization.objects.create(attributes='')
        self.period.division_set.create(object_id=self.organization.id)

        self.document = Document.objects.create(period=self.period, object_id=self.organization.id)
        self.document.sheets.set([self.form1, self.form2])
        for i, column in enumerate(self.form2_columns, 1):
            Value.objects.create(
                document=self.document,
                sheet=self.form2,
                column=column,
                row=self.form2_row,
                value=f'{i:.1f}',
            )

        self.default_values = (
            ('11.0', False),
            ('2.0', False),
            ('3.0', False),
            ('1.0', True),
            ('2.0', True),
            ('3.0', True),
        )

    def test_add_formula_not_recalculate(self) -> None:
        """Тестирование добавления формулы без пересчета значений в документах."""
        self._test_values(self.default_values)
        change_cell_formula(self.superuser, self.form1_cells[1], "=СУММ('Форма №2'!A1:C1)", False)
        self._test_values(self.default_values)
        update_or_create_values(
            self.superuser,
            self.document,
            self.form2.id,
            [ValueInput(cell=self.form2_cells[2], value='4.0')]
        )
        self._test_values((
            ('17.0', True),
            ('7.0', True),
            ('3.0', False),
            ('1.0', True),
            ('2.0', True),
            ('4.0', True),
        ))

    def test_add_formula_recalculate(self) -> None:
        """Тестирование добавления формулы с перерасчетом значений в документах."""
        self._test_values(self.default_values)
        change_cell_formula(self.superuser, self.form1_cells[1], "=СУММ('Форма №2'!A1:C1)", True)
        self._test_values((
            ('15.0', True),
            ('6.0', True),
            ('3.0', False),
            ('1.0', True),
            ('2.0', True),
            ('3.0', True),
        ))

    def test_change_formula_not_recalculate(self) -> None:
        """Тестирование изменения формулы без перерасчета значений в документах."""
        self._test_values(self.default_values)
        change_cell_formula(self.superuser, self.form1_cells[0], "=СУММ(B1:C1) + СУММ('Форма №2'!A1:C1) + 10", False)
        self._test_values(self.default_values)
        update_or_create_values(
            self.superuser,
            self.document,
            self.form2.id,
            [ValueInput(cell=self.form2_cells[2], value='4.0')]
        )
        self._test_values((
            ('22.0', True),
            ('2.0', False),
            ('3.0', False),
            ('1.0', True),
            ('2.0', True),
            ('4.0', True),
        ))

    def test_change_formula_recalculate(self) -> None:
        """Тестирование изменения формулы с перерасчетом значений в документах."""
        self._test_values(self.default_values)
        change_cell_formula(self.superuser, self.form1_cells[0], "=СУММ(B1:C1) + СУММ('Форма №2'!A1:C1) + 10", True)
        self._test_values((
            ('21.0', True),
            ('2.0', False),
            ('3.0', False),
            ('1.0', True),
            ('2.0', True),
            ('3.0', True),
        ))

    def test_delete_formula_not_recalculate(self) -> None:
        """Тестирование удаления формулы без перерасчета значений в документах."""
        self._test_values(self.default_values)
        change_cell_formula(self.superuser, self.form1_cells[0], '', False)
        self._test_values(self.default_values)
        update_or_create_values(
            self.superuser,
            self.document,
            self.form2.id,
            [ValueInput(cell=self.form2_cells[2], value='4.0')]
        )
        self._test_values((
            ('11.0', False),
            ('2.0', False),
            ('3.0', False),
            ('1.0', True),
            ('2.0', True),
            ('4.0', True),
        ))

    def test_delete_formula_recalculate(self) -> None:
        """Тестирование удаления формулы с перерасчетом значений в документах."""
        self._test_values(self.default_values)
        change_cell_formula(self.superuser, self.form1_cells[0], '', True)
        self._test_values(self.default_values)

    def _test_values(self, values: Iterable[tuple[str, bool]]) -> None:
        """Тестирование значений ячеек."""
        for column, value_exist in zip([*self.form1_columns, *self.form2_columns], values):
            expected_value, exist = value_exist
            value = Value.objects.filter(document=self.document, column=column).first()
            self.assertEqual(exist, bool(value))
            actual_value = value.value if value else Cell.objects.filter(column=column).first().default
            self.assertEqual(expected_value, actual_value)


class PasteTestCase(TestCase):
    """Тестирование функции `paste_into_cells`."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.organization_content_type = ContentType.objects.get_for_model(Organization)
        self.project = Project.objects.create(content_type=self.organization_content_type)
        self.period = Period.objects.create(project=self.project)
        self.sheet = Sheet.objects.create(name='Форма', period=self.period)
        self.columns = [ColumnDimension.objects.create(index=i, sheet=self.sheet) for i in range(1, 3)]
        self.rows = [RowDimension.objects.create(index=i, sheet=self.sheet) for i in range(1, 3)]
        self.cells: dict[(int, int), Cell] = {}
        for row in self.rows:
            for column in self.columns:
                self.cells[(row.index, column.index)] = Cell.objects.create(
                    kind=KindCell.NUMERIC,
                    default='0.0',
                    column=column,
                    row=row,
                )

    def test_single_cell_without_style(self) -> None:
        """Тестирование вставки в одиночную ячейку без изменения стилей."""
        cell = self.cells[1, 1]
        actual_cells = paste_into_cells([CellPasteOptions(cell=cell, default='2.0', style=None)])
        self.assertEqual([cell], actual_cells)
        actual_cell = actual_cells[0]
        self.assertEqual('2.0', actual_cell.default)
        self.assertFalse(actual_cell.strong)
        self.assertFalse(actual_cell.italic)
        self.assertIsNone(actual_cell.underline)
        self.assertFalse(actual_cell.strike)
        self.assertIsNone(actual_cell.horizontal_align)
        self.assertIsNone(actual_cell.vertical_align)
        self.assertEqual(12, actual_cell.size)

    def test_single_cell_with_style(self) -> None:
        """Тестирование вставки в одиночную ячейку с изменением стилей."""
        cell = self.cells[1, 1]
        actual_cells = paste_into_cells([CellPasteOptions(
            cell=cell,
            default='2.0',
            style=CellPasteStyle(
                strong=True,
                italic=True,
                underline=Style.SINGLE,
                strike=True,
                horizontal_align=Style.LEFT,
                vertical_align=Style.TOP,
                size=20,
                color='#FF0000',
                background='#00FF00',
            ),
        )])
        self.assertEqual([cell], actual_cells)
        actual_cell = actual_cells[0]
        self.assertEqual('2.0', actual_cell.default)
        self.assertTrue(actual_cell.strong)
        self.assertTrue(actual_cell.italic)
        self.assertEqual(Style.SINGLE, actual_cell.underline)
        self.assertTrue(actual_cell.strike)
        self.assertEqual(Style.LEFT, actual_cell.horizontal_align)
        self.assertEqual(Style.TOP, actual_cell.vertical_align)
        self.assertEqual(20, actual_cell.size)
        self.assertEqual('#FF0000', actual_cell.color)
        self.assertEqual('#00FF00', actual_cell.background)

    def test_multiple_cells(self) -> None:
        """Тестирование вставки в несколько ячеек."""
        cells = self.cells.values()
        actual_cells = paste_into_cells([CellPasteOptions(
            cell=cell,
            default=f'{i:.1f}',
            style=CellPasteStyle(
                strong=True,
                italic=False,
                underline=None,
                strike=False,
                horizontal_align=Style.LEFT,
                vertical_align=Style.TOP,
                size=10 + i,
                color='#FF0000',
                background='#00FF00',
            )
        ) for i, cell in enumerate(cells)])
        self.assertEqual(set(cells), set(actual_cells))
        for i, actual_cell in enumerate(actual_cells):
            self.assertEqual(f'{i:.1f}', actual_cell.default)
            self.assertTrue(actual_cell.strong)
            self.assertFalse(actual_cell.italic)
            self.assertIsNone(actual_cell.underline)
            self.assertFalse(actual_cell.strike)
            self.assertEqual(Style.LEFT, actual_cell.horizontal_align)
            self.assertEqual(Style.TOP, actual_cell.vertical_align)
            self.assertEqual(10 + i, actual_cell.size)
            self.assertEqual('#FF0000', actual_cell.color)
            self.assertEqual('#00FF00', actual_cell.background)
