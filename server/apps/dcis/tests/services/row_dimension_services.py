"""Тесты модуля, отвечающего за работу со строками."""
from itertools import product
from unittest.mock import patch

from django.core.exceptions import PermissionDenied

from apps.dcis.models import Cell, ColumnDimension, Document, MergedCell, RowDimension
from apps.dcis.services.row_dimension_services import (
    change_row_dimension,
    change_row_dimensions_fixed,
    get_relative_rows,
)
from .common import TableTestCase


class RowDimensionTestCase(TableTestCase):
    """Тесты модуля, отвечающего за работу со строками."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        super().setUp()

        self.document = Document.objects.create(period=self.period)

        self.root_row_dimension = RowDimension.objects.create(sheet=self.sheet, dynamic=True, index=1)
        self.root_row_dimension_change_data = {
            'height': 10,
            'hidden': True,
            'dynamic': True
        }

        self.root_row_dimensions = [RowDimension.objects.create(sheet=self.sheet, index=i) for i in range(2, 5)]
        self.column_dimensions = [ColumnDimension.objects.create(sheet=self.sheet, index=i) for i in range(1, 5)]
        for row, column in product(
            [self.root_row_dimension, *self.root_row_dimensions],
            self.column_dimensions
        ):
            Cell.objects.create(row=row, column=column)

        self.large_merged_cell = MergedCell.objects.create(min_col=1, min_row=2, max_col=2, max_row=4, sheet=self.sheet)
        self.small_merged_cell = MergedCell.objects.create(min_col=3, min_row=3, max_col=3, max_row=4, sheet=self.sheet)

    def test_change_row_dimension(self) -> None:
        """Тестирование функции `change_row_dimension`."""
        with patch.object(
            self.superuser, 'has_perm', new=lambda perm: perm != 'dcis.change_sheet'
        ), self.assertRaises(PermissionDenied):
            change_row_dimension(
                user=self.superuser,
                row_dimension=self.root_row_dimension,
                **self.root_row_dimension_change_data,
            )
        changed_row = change_row_dimension(
            user=self.superuser,
            row_dimension=self.root_row_dimension,
            **self.root_row_dimension_change_data,
        )
        self.assertEqual(self.root_row_dimension, changed_row)
        for k, v in self.root_row_dimension_change_data.items():
            self.assertEqual(v, getattr(changed_row, k))

    def test_get_relative_rows(self) -> None:
        """Тестирование функции `get_relative_rows`."""
        self.assertEqual([self.root_row_dimension], get_relative_rows(self.root_row_dimension))
        for row in self.root_row_dimensions:
            self.assertEqual(self.root_row_dimensions, get_relative_rows(row))

    def test_change_row_dimension_fixed_first_row(self) -> None:
        """Тестирование функции `change_row_dimension_fixed` для первой строки."""
        for value in (True, False):
            changed_rows = change_row_dimensions_fixed([self.root_row_dimension], value)
            self.assertEqual(
                [self.root_row_dimension],
                changed_rows
            )
            for changed_row in changed_rows:
                self.assertEqual(changed_row.fixed, value)
            for row in self.root_row_dimensions:
                self.assertFalse(row.fixed)

    def test_change_row_dimension_fixed_middle_row(self) -> None:
        """Тестирование функции `change_row_dimension_fixed` для строки в середине."""
        for value in (True, False):
            changed_rows = change_row_dimensions_fixed([self.root_row_dimensions[1]], value)
            self.assertEqual(
                set(self.root_row_dimensions),
                set(changed_rows)
            )
            for changed_row in changed_rows:
                self.assertEqual(changed_row.fixed, value)
            self.root_row_dimension.refresh_from_db()
            self.assertEqual(self.root_row_dimension.fixed, False)
