"""Тестирование модуля, отвечающего за работу с листами."""

from devind_dictionaries.models import Organization
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.dcis.models import Cell, ColumnDimension, Period, Project, RowDimension, Sheet
from apps.dcis.models.sheet import KindCell, Style
from apps.dcis.services.sheet_services import CellPasteOptions, CellPasteStyle, CheckCellOptions, paste_into_cells


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
                self.cells[(row.index, row.index)] = Cell.objects.create(
                    kind=KindCell.NUMERIC,
                    default='0.0',
                    column=column,
                    row=row
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
                size=10 + i
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
