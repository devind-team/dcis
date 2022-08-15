"""Тесты модуля, отвечающего за работу с колонками."""
from itertools import product
from unittest.mock import patch

from django.core.exceptions import PermissionDenied

from apps.dcis.models import Cell, ColumnDimension, MergedCell, RowDimension
from .common import TableTestCase
from ...services.column_dimension_services import (
    change_column_dimension,
    change_column_dimension_fixed,
    get_relative_columns,
)


class ColumnDimensionTestCase(TableTestCase):
    """Тесты модуля, отвечающего за работу с колонками."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        super().setUp()

        self.column_dimension = ColumnDimension.objects.create(sheet=self.sheet, index=1)
        self.column_dimension_change_data = {
            'width': 10,
            'fixed': True,
            'hidden': True,
            'kind': 'n'
        }

        self.column_dimensions = [ColumnDimension.objects.create(sheet=self.sheet, index=i) for i in range(2, 5)]
        self.extra_column_dimension = ColumnDimension.objects.create(sheet=self.sheet, index=5)
        self.row_dimensions = [RowDimension.objects.create(sheet=self.sheet, index=i) for i in range(1, 5)]
        for column, row in product(
            [self.column_dimension, *self.column_dimensions, self.extra_column_dimension],
            self.row_dimensions
        ):
            Cell.objects.create(row=row, column=column)

        self.large_merged_cell = MergedCell.objects.create(min_col=2, min_row=1, max_col=4, max_row=2, sheet=self.sheet)
        self.small_merged_cell = MergedCell.objects.create(min_col=3, min_row=3, max_col=4, max_row=3, sheet=self.sheet)

    def test_get_relative_columns(self) -> None:
        """Тестирование функции `get_relative_columns`."""
        self.assertEqual([self.column_dimension], get_relative_columns(self.column_dimension))
        for column in self.column_dimensions:
            self.assertEqual(self.column_dimensions, get_relative_columns(column))

    def test_change_column_dimension_fixed(self) -> None:
        """Тестирование функции `change_column_dimension_fixed`."""
        changed_columns = change_column_dimension_fixed(self.column_dimensions[1], True)
        self.assertEqual({self.column_dimension, *self.column_dimensions}, set(changed_columns))
        for changed_column in changed_columns:
            self.assertTrue(changed_column.fixed)
        self.extra_column_dimension.refresh_from_db()
        self.assertFalse(self.extra_column_dimension.fixed)
        changed_columns = change_column_dimension_fixed(self.column_dimensions[1], False)
        self.assertEqual(set(self.column_dimensions), set(changed_columns))
        self.column_dimension.refresh_from_db()
        self.assertTrue(self.column_dimension.fixed)
        for changed_column in changed_columns:
            self.assertFalse(changed_column.fixed)
        self.extra_column_dimension.refresh_from_db()
        self.assertFalse(self.extra_column_dimension.fixed)

    def test_change_column_dimension(self) -> None:
        """Тестирование функции `change_column_dimension`."""
        with patch.object(
            self.superuser, 'has_perm', new=lambda perm: perm != 'dcis.change_sheet'
        ), self.assertRaises(PermissionDenied):
            change_column_dimension(
                user=self.superuser,
                column_dimension=self.column_dimension,
                **self.column_dimension_change_data,
            )
        changed_columns = change_column_dimension(
            user=self.superuser,
            column_dimension=self.column_dimension,
            **self.column_dimension_change_data,
        )
        self.assertEqual({self.column_dimension}, set(changed_columns))
        for k, v in self.column_dimension_change_data.items():
            self.assertEqual(v, getattr(changed_columns[0], k))
