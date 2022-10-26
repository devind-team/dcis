"""Тесты модуля, отвечающего за работу со статусами."""
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase, override_settings

from apps.core.models import User
from apps.dcis.models import (
    AddStatus,
    Cell, ColumnDimension,
    Document,
    DocumentStatus,
    Limitation, Period,
    Project,
    RowDimension,
    Sheet,
    Status, Value,
)
from apps.dcis.services.status_services import AddStatusCheck, add_document_status, delete_document_status


class StatusTestCase(TestCase):
    """Тестирование разных функций работы со статусами."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)

        self.status_to_add = Status.objects.create(name='add_status')
        self.exist_status = Status.objects.create(name='exist_status')
        self.add_status = AddStatus.objects.create(
            from_status=self.exist_status,
            to_status=self.status_to_add,
            roles=[],
            check='test_check',
        )
        self.add_document = Document.objects.create(user=self.superuser, period=self.period)
        self.add_document_status = DocumentStatus.objects.create(
            user=self.superuser,
            document=self.add_document,
            status=self.exist_status,
        )

        self.status_to_delete = Status.objects.create(name='delete_status')
        self.delete_document = Document.objects.create(period=self.period)
        self.delete_document_status = DocumentStatus.objects.create(
            user=self.superuser,
            document=self.delete_document,
            status=self.status_to_delete,
        )

    def test_add_document_status(self) -> None:
        """Тестирование функции `add_document_status`."""
        with patch.object(
            self.superuser, 'has_perm', new=lambda perm: perm != 'dcis.change_document'
        ), self.assertRaises(PermissionDenied):
            self._add_document_status()
        with patch(
            'apps.dcis.services.status_services.AddStatusCheck.test_check',
            create=True,
            new=Mock()
        ) as mock:
            actual_document_status = self._add_document_status()
            mock.assert_called_once_with(self.add_document)
        expected_document_status = DocumentStatus.objects.get(comment='Add document status')
        self.assertEqual(expected_document_status, actual_document_status)

    def test_delete_document_status(self) -> None:
        """Тестирование функции `delete_document_status`."""
        with patch.object(
            self.superuser, 'has_perm', new=lambda perm: perm != 'dcis.change_document'
        ), self.assertRaises(PermissionDenied):
            self._delete_document_status()
        self.assertIsNone(delete_document_status(user=self.superuser, status=self.delete_document_status))

    def _add_document_status(self) -> DocumentStatus:
        """Добавление статуса документа."""
        return add_document_status(
            user=self.superuser,
            document=self.add_document,
            status=self.status_to_add,
            comment='Add document status'
        )

    def _delete_document_status(self) -> None:
         """Удаление статуса документа."""
         delete_document_status(user=self.superuser, status=self.delete_document_status)


class AddStatusCheckTestCase(TestCase):
    """Тестирование класса `AddStatusCheck`."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""

        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)

        self.sheet1 = Sheet.objects.create(period=self.period, name='sheet1')
        self.sheet1_row = RowDimension.objects.create(index=1, sheet=self.sheet1)
        self.sheet1_columns = [ColumnDimension.objects.create(index=i, sheet=self.sheet1) for i in range(1, 4)]
        self.sheet1_cells = {
            'A1': Cell.objects.create(column=self.sheet1_columns[0], row=self.sheet1_row),
            'B1': Cell.objects.create(column=self.sheet1_columns[1], row=self.sheet1_row),
            'C1': Cell.objects.create(formula='=A1+B1', column=self.sheet1_columns[2], row=self.sheet1_row),
        }

        self.sheet2 = Sheet.objects.create(period=self.period, name='sheet2')
        self.sheet2_rows = [RowDimension.objects.create(index=i, sheet=self.sheet2) for i in range(1, 3)]
        self.sheet2_column = ColumnDimension.objects.create(index=1, sheet=self.sheet2)
        self.sheet2_cells = {
            'A1': Cell.objects.create(formula='=sheet1!A1', column=self.sheet2_column, row=self.sheet2_rows[0]),
            'A2': Cell.objects.create(column=self.sheet2_column, row=self.sheet2_rows[1]),
        }

        self.limitations = [
            Limitation.objects.create(
                formula='sheet1!C1 > 5',
                error_message='sheet1!C1 больше 5',
                sheet=self.sheet1
            ),
            Limitation.objects.create(
                formula='2 / sheet2!A1 > 0.2',
                error_message='sheet2!A1 больше 0.2',
                sheet=self.sheet2
            ),
            Limitation.objects.create(
                formula='sheet2!A2 < sheet1!C1',
                error_message='sheet2!A2 меньше sheet1!C1',
                sheet=self.sheet2
            ),
        ]

        self.document_with_calculation_errors = self._create_document(['0', '6', '6', '0', '3'])
        self.document_with_limitation_errors = self._create_document(['1', '2', '3', '1', '4'])
        self.document_without_errors = self._create_document(['3', '4', '7', '3', '5'])

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
    def test_check_limitations_with_calculation_errors(self) -> None:
        """Тестирование функции `check_limitations` с ошибками вычислений."""
        with self.assertRaises(ValidationError) as error:
            AddStatusCheck.check_limitations(self.document_with_calculation_errors)
        self.assertEqual({'limitations': list(map(ValidationError, ['Деление на 0']))}, error.exception.error_dict)

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
    def test_check_limitations_with_limitation_errors(self) -> None:
        """Тестирование функции `check_limitations` с ошибками ограничений."""
        with self.assertRaises(ValidationError) as error:
            AddStatusCheck.check_limitations(self.document_with_limitation_errors)
        self.assertEqual(
            {'limitations': list(map(ValidationError, ['sheet1!C1 больше 5', 'sheet2!A2 меньше sheet1!C1']))},
            error.exception.error_dict
        )

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
    def test_check_limitations(self) -> None:
        """Тестирование функции `check_limitations` без ошибок."""
        AddStatusCheck.check_limitations(self.document_without_errors)

    def _create_document(self, values: list[str]) -> Document:
        """Создание документа со значениями."""
        document = Document.objects.create(period=self.period)
        document.sheets.set([self.sheet1, self.sheet2])
        for i in range(3):
            Value.objects.create(
                value=values[i],
                document=document,
                sheet=self.sheet1,
                column=self.sheet1_columns[i],
                row=self.sheet1_row
            )
        for i in range(2):
            Value.objects.create(
                value=values[3 + i],
                document=document,
                sheet=self.sheet2,
                column=self.sheet2_column,
                row=self.sheet2_rows[i]
            )
        return document
