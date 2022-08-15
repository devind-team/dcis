"""Тесты модуля, отвечающего за работу со строками."""
from itertools import product
from unittest.mock import patch

from django.core.exceptions import PermissionDenied

from apps.dcis.models import Cell, ColumnDimension, Document, MergedCell, RowDimension
from apps.dcis.services.row_dimension_services import (
    change_row_dimension,
    change_row_dimension_fixed,
    get_relative_rows,
    is_ancestor,
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
            'fixed': True,
            'hidden': True,
            'dynamic': True
        }

        self.child_row_dimension = RowDimension.objects.create(
            sheet=self.sheet,
            document=self.document,
            index=1,
            dynamic=True,
            parent=self.root_row_dimension
        )
        self.descendant_row_dimension = RowDimension.objects.create(
            sheet=self.sheet,
            document=self.document,
            index=1,
            dynamic=True,
            parent=self.child_row_dimension,
        )

        self.root_row_dimensions = [RowDimension.objects.create(sheet=self.sheet, index=i) for i in range(2, 5)]
        self.extra_root_dimension = RowDimension.objects.create(sheet=self.sheet, index=5)
        self.column_dimensions = [ColumnDimension.objects.create(sheet=self.sheet, index=i) for i in range(1, 5)]
        for row, column in product(
            [self.root_row_dimension, *self.root_row_dimensions, self.extra_root_dimension],
            self.column_dimensions
        ):
            Cell.objects.create(row=row, column=column)

        self.large_merged_cell = MergedCell.objects.create(min_col=1, min_row=2, max_col=2, max_row=4, sheet=self.sheet)
        self.small_merged_cell = MergedCell.objects.create(min_col=3, min_row=3, max_col=3, max_row=4, sheet=self.sheet)

    def test_is_ancestor(self) -> None:
        """Тестирование функции `is_ancestor`."""
        self.assertTrue(is_ancestor(self.root_row_dimension, self.child_row_dimension))
        self.assertTrue(is_ancestor(self.root_row_dimension, self.descendant_row_dimension))
        self.assertFalse(is_ancestor(self.root_row_dimensions[0], self.root_row_dimension))
        self.assertFalse(is_ancestor(self.root_row_dimensions[0], self.child_row_dimension))
        self.assertFalse(is_ancestor(self.root_row_dimensions[0], self.descendant_row_dimension))

    def test_get_relative_rows(self) -> None:
        """Тестирование функции `get_relative_rows`."""
        self.assertEqual([self.root_row_dimension], get_relative_rows(self.root_row_dimension))
        for row in self.root_row_dimensions:
            self.assertEqual(self.root_row_dimensions, get_relative_rows(row))

    def test_change_row_dimension_fixed_first_row(self) -> None:
        """Тестирование функции `change_row_dimension_fixed` для первой строки."""
        for value in (True, False):
            changed_rows = change_row_dimension_fixed(self.root_row_dimension, value)
            self.assertEqual(
                {self.root_row_dimension, self.child_row_dimension, self.descendant_row_dimension},
                set(changed_rows)
            )
            for changed_row in changed_rows:
                self.assertEqual(changed_row.fixed, value)
            for row in self.root_row_dimensions:
                self.assertFalse(row.fixed)

    def test_change_row_dimension_fixed_middle_row(self) -> None:
        """Тестирование функции `change_row_dimension_fixed` для строки в середине."""
        changed_rows = change_row_dimension_fixed(self.root_row_dimensions[1], True)
        self.assertEqual(
            {
                self.root_row_dimension,
                self.child_row_dimension,
                self.descendant_row_dimension,
                *self.root_row_dimensions
            },
            set(changed_rows)
        )
        for changed_row in changed_rows:
            self.assertTrue(changed_row.fixed)
        self.extra_root_dimension.refresh_from_db()
        self.assertFalse(self.extra_root_dimension.fixed)
        changed_rows = change_row_dimension_fixed(self.root_row_dimensions[1], False)
        self.assertEqual(set(self.root_row_dimensions), set(changed_rows))
        for row in (
            self.root_row_dimension,
            self.child_row_dimension,
            self.descendant_row_dimension,
        ):
            row.refresh_from_db()
            self.assertTrue(row.fixed)
        for changed_row in changed_rows:
            self.assertFalse(changed_row.fixed)
        self.extra_root_dimension.refresh_from_db()
        self.assertFalse(self.extra_root_dimension.fixed)

    def test_change_row_dimension_without_document_ids(self) -> None:
        """Тестирование функции `change_row_dimension` без идентификаторов документов."""
        with patch.object(
            self.superuser, 'has_perm', new=lambda perm: perm != 'dcis.change_sheet'
        ), self.assertRaises(PermissionDenied):
            change_row_dimension(
                user=self.superuser,
                row_dimension=self.root_row_dimension,
                **self.root_row_dimension_change_data,
                document_ids=[],
            )
        changed_rows = change_row_dimension(
            user=self.superuser,
            row_dimension=self.root_row_dimension,
            **self.root_row_dimension_change_data,
            document_ids=[],
        )
        self.assertEqual({self.root_row_dimension}, set(changed_rows))
        for k, v in self.root_row_dimension_change_data.items():
            self.assertEqual(v, getattr(changed_rows[0], k))

    def test_change_row_dimension_with_document_ids(self) -> None:
        """Тестирование функции `change_row_dimension` с идентификаторами документов."""
        changed_rows = change_row_dimension(
            user=self.superuser,
            row_dimension=self.root_row_dimension,
            **self.root_row_dimension_change_data,
            document_ids=[self.document.id],
        )
        self.assertEqual(
            {self.root_row_dimension, self.child_row_dimension, self.descendant_row_dimension},
            set(changed_rows)
        )
        self.root_row_dimension.refresh_from_db()
        for k, v in self.root_row_dimension_change_data.items():
            self.assertEqual(v, getattr(self.root_row_dimension, k))
