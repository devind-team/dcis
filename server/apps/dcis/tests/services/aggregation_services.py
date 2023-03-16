"""Тесты модуля, отвечающего за работу с ячейками."""

import json
from os import listdir, remove
from os.path import isfile, join
from unittest.mock import MagicMock, patch

from devind_dictionaries.models import Organization
from devind_helpers.schema.types import ErrorFieldType
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import (
    Cell,
    ColumnDimension,
    Period,
    Project,
    RelationshipCells,
    RowDimension,
    Sheet,
)
from apps.dcis.services.aggregation_services import (
    add_aggregation_cell,
    add_cell_aggregation,
    check_cell_permission,
    delete_cells_aggregation,
    dependent_cells,
    get_cells_aggregation,
    transformation_position_cell,
    unload_aggregations_in_file, update_aggregations_from_file,
)


class AggregationTestCase(TestCase):
    """Тестирование агрегации."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""

        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.organization_content_type = ContentType.objects.get_for_model(Organization)
        self.project = Project.objects.create(content_type=self.organization_content_type)

        self.add_period = Period.objects.create(project=self.project)
        self.add_period_form1 = Sheet.objects.create(name='Форма1', period=self.add_period)
        self.add_period_form1_row = [
            RowDimension.objects.create(sheet=self.add_period_form1, index=i) for i in range(1, 4)
        ]
        self.add_period_form1_column = ColumnDimension.objects.create(sheet=self.add_period_form1, index=1)
        self.form1_cells = [
            Cell.objects.create(row=row, column=self.add_period_form1_column) for row in self.add_period_form1_row
        ]
        self.form1_cell_aggregation = Cell.objects.get(id=self.form1_cells[0].id)
        self.form1_cell_aggregation.aggregation = 'sum'
        self.form1_cell_aggregation.save()

        self.add_period_form2 = Sheet.objects.create(name='Форма2', period=self.add_period)
        self.add_period_form2_row = [
            RowDimension.objects.create(sheet=self.add_period_form2, index=i) for i in range(1, 4)
        ]
        self.add_period_form2_column = ColumnDimension.objects.create(sheet=self.add_period_form2, index=1)
        self.form2_cells = [
            Cell.objects.create(row=row, column=self.add_period_form2_column) for row in self.add_period_form2_row
        ]

    def test_check_cell_permission(self):
        """Тестирование функции `check_cell_permission`."""

        cell = check_cell_permission(self.superuser, self.form1_cells[0].pk)
        self.assertEqual(cell, self.form1_cells[0])

    def test_add_cell_aggregation_table(self):
        """Тестирование функции `add_cell_aggregation`."""
        result, errors = add_cell_aggregation(
            self.superuser,
            self.form1_cell_aggregation.pk,
            [self.form1_cells[1].id, self.form1_cells[2].id]
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], self.form1_cells[1])
        self.assertEqual(len(errors), 0)

    def test_add_cell_aggregation_cell_not_aggregating(self):
        """Тестирование функции `add_cell_aggregation`без агрегации."""
        error = ([], [ErrorFieldType('cell', ['Ячейка не является агрегирующей'])])
        self.assertEqual(
            add_cell_aggregation(
                self.superuser,
                self.form2_cells[0].id,
                [self.form2_cells[1].id, self.form2_cells[2].id]
            ), error
        )

    def test_get_cells_aggregation(self):
        """Тестирование функции `get_cells_aggregation`."""
        result = get_cells_aggregation(self.superuser, self.add_period)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, f'{self.form1_cell_aggregation.id}')
        self.assertEqual(result[0].position, transformation_position_cell(self.form1_cell_aggregation))
        self.assertEqual(result[0].aggregation, 'sum')
        self.assertEqual(result[0].cells, [])

    def test_get_cells_aggregation_no_cells(self):
        """Тестирование функции `get_cells_aggregation` без агрегации."""
        period = Period.objects.create(project=self.project, name='testperiod')
        result = get_cells_aggregation(self.superuser, period)
        self.assertEqual(len(result), 0)

    def test_get_cells_aggregation_permission(self):
        """Тестирование функции `get_cells_aggregation` на права."""
        with patch.object(
            self.superuser, 'has_perm', lambda perm: perm != 'dcis.change_period'
        ), self.assertRaises(PermissionDenied):
            get_cells_aggregation(self.superuser, self.add_period)

    def test_transformation_position_cell(self):
        """Тестирование функции `transformation_position_cell`."""
        position = transformation_position_cell(self.form1_cell_aggregation)
        self.assertEqual(position, "'Форма1'!A1")

    def test_dependent_cells(self):
        """Тестирование функции `dependent_cells`."""
        add_cell_aggregation(
            self.superuser,
            self.form1_cell_aggregation.pk,
            [self.form2_cells[1].id, self.form2_cells[2].id]
        )
        result = dependent_cells(self.form1_cell_aggregation.to_cells.all())
        self.assertListEqual(result, ["'Форма2'!A2", "'Форма2'!A3"])

    def test_add_aggregation_cell(self):
        """Тестирование функции `add_aggregation_cell`."""
        aggregation_cell = "'Форма2'!A1"
        aggregation_method = 'avg'
        aggregation_cells = ["'Форма2'!A2", "'Форма2'!A3"]

        result = add_aggregation_cell(
            self.superuser,
            self.add_period,
            aggregation_cell,
            aggregation_method,
            aggregation_cells
        )

        self.assertEqual(result.aggregation, aggregation_method)
        self.assertEqual(result.position, aggregation_cell)
        self.assertEqual(result.cells, result.cells)

        updated_cell = Cell.objects.get(
            column__sheet__period=self.add_period,
            column__sheet__name='Форма2',
            column__index=1,
            row__index=1
        )
        self.assertEqual(updated_cell.aggregation, 'avg')

    def test_delete_cells_aggregation(self):
        """Тестирование функции `delete_cells_aggregation`."""
        delete_cells_aggregation(self.superuser, self.form1_cell_aggregation.id)
        self.assertFalse(RelationshipCells.objects.filter(to_cell=self.form1_cell_aggregation.id).exists())
        self.form1_cell_aggregation.refresh_from_db()
        self.assertIsNone(self.form1_cell_aggregation.aggregation)

    def test_update_aggregations_from_file(self) -> None:
        """Тестирование функции `update_aggregations_from_file`."""
        file_data = [
            {
                'to_cell': "'Форма1'!A1",
                'aggregation': "avg",
                'from_cells': [
                    "'Форма2'!A2",
                    "'Форма1'!A3"
                ]
            },
            {
                'to_cell': "'Форма2'!A1",
                'aggregation': 'sum',
                'from_cells': [
                    "'Форма1'!A2",
                    "'Форма1'!A3"
                ]
            }
        ]

        file = SimpleUploadedFile('aggregation.json', bytes(json.dumps(file_data), 'utf-8'))

        result = update_aggregations_from_file(self.superuser, self.add_period, file)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].aggregation, file_data[0]['aggregation'])
        self.assertEqual(result[0].position, file_data[0]['to_cell'])
        self.assertEqual(result[0].cells, ["'Форма1'!A3", "'Форма2'!A2"])
        self.assertEqual(result[1].aggregation, file_data[1]['aggregation'])
        self.assertEqual(result[1].position, file_data[1]['to_cell'])
        self.assertEqual(result[1].cells, file_data[1]['from_cells'])

    def test_update_aggregations_from_file_invalid_data(self):
        """Тестирование функции `update_aggregations_from_file` на недопустимые значения JSON."""
        file = SimpleUploadedFile(
            'aggregation.json',
            b'[{"from_cells": "invalid", "to_cell": "invalid", "aggregation": "invalid"}]'
        )

        with self.assertRaises(ValueError) as context:
            update_aggregations_from_file(self.superuser, self.add_period, file)

        self.assertIn('Недопустимые данные JSON:', str(context.exception))

    def test_unload_aggregations_in_file(self):
        """Тестирование функции `unload_attributes_in_file`."""
        get_host = MagicMock(return_value='http://testserver')
        result = unload_aggregations_in_file(self.superuser, get_host, self.add_period)

        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith('.json'))

        with open(join(settings.BASE_DIR, result)) as file:
            data = json.load(file)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def tearDown(self):
        """Remove the temporary files created during the test."""
        temp_dir = join(settings.STATICFILES_DIRS[1], 'temp_files')
        for file in listdir(temp_dir):
            file_path = join(temp_dir, file)
            if isfile(file_path):
                remove(file_path)
