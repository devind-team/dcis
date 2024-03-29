"""Тесты модуля, отвечающего за работу со статусами."""

from itertools import product
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase, override_settings
from jsonpickle import encode

from apps.core.models import User
from apps.dcis.models import (
    AddStatus,
    Cell,
    ColumnDimension,
    Document,
    DocumentStatus,
    Limitation,
    Period,
    Project,
    RowDimension,
    Sheet,
    Status,
    Value,
)
from apps.dcis.services.status_services import (
    AddStatusActions,
    LimitationError,
    StatusAction,
    add_document_status,
    delete_document_status,
    get_initial_statuses,
    get_new_statuses,
)


class StatusTestCase(TestCase):
    """Тестирование разных функций работы со статусами."""

    class TestAction(StatusAction):
        """Тестовое действие при добавлении статуса."""

        pre_mock: Mock = Mock()
        post_mock: Mock = Mock()

        @classmethod
        def pre_execute(cls, document: Document) -> None:
            cls.pre_mock(document)

        @classmethod
        def post_execute(cls, document: Document, document_status: DocumentStatus) -> None:
            cls.post_mock(document, document_status)

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)
        self.document = Document.objects.create(period=self.period)

        self.initial_status = Status.objects.create(name='initial_status')
        self.initial_add_status = AddStatus.objects.create(
            from_status=None,
            to_status=self.initial_status,
            roles=[]
        )
        self.initial_admin_status = Status.objects.create(name='initial_admit_status')
        self.initial_admin_add_status = AddStatus.objects.create(
            from_status=None,
            to_status=self.initial_admin_status,
            roles=['admin']
        )
        self.initial_division_member_status = Status.objects.create(name='initial_division_member_status')
        self.initial_division_member_add_status = AddStatus.objects.create(
            from_status=None,
            to_status=self.initial_division_member_status,
            roles=['division_member']
        )
        self.initial_admin_division_member_status = Status.objects.create(name='initial_admit_division_member_status')
        self.initial_admin_division_member_add_status = AddStatus.objects.create(
            from_status=None,
            to_status=self.initial_admin_division_member_status,
            roles=['admin', 'division_member']
        )

        self.document_current_status = Status.objects.create(name='document_current_status')
        self.document_status = DocumentStatus.objects.create(
            document=self.document,
            status=self.document_current_status,
            user=self.superuser,
        )
        self.new_statuses = [Status.objects.create(name=f'new_status{i}') for i in range(1, 5)]
        for i, new_status in enumerate(self.new_statuses, 1):
            AddStatus.objects.create(
                from_status=self.document_current_status,
                to_status=new_status,
                roles=['creator', 'curator', 'division_member', 'admin'][0:i]
            )

        self.status_to_add = Status.objects.create(name='status_to_add')
        self.exist_status = Status.objects.create(name='exist_status')
        self.add_status = AddStatus.objects.create(
            from_status=self.exist_status,
            to_status=self.status_to_add,
            roles=['admin'],
            action='TestAction',
        )
        self.add_document = Document.objects.create(user=self.superuser, period=self.period)
        self.add_document_status = DocumentStatus.objects.create(
            document=self.add_document,
            status=self.exist_status,
            user=self.superuser,
        )

        self.status_to_delete = Status.objects.create(name='delete_status')
        self.delete_document = Document.objects.create(period=self.period)
        self.delete_document_status = DocumentStatus.objects.create(
            user=self.superuser,
            document=self.delete_document,
            status=self.status_to_delete,
        )

    def test_get_initial_statuses(self) -> None:
        """Тестирование функции `get_initial_statuses`."""
        self.assertQuerysetEqual(
            Status.objects.none(),
            get_initial_statuses(self.user, self.period)
        )
        self.assertEqual(
            {self.initial_admin_status, self.initial_admin_division_member_status},
            set(get_initial_statuses(self.superuser, self.period))
        )
        with patch(
            'apps.dcis.services.status_services.is_period_division_member',
            new=Mock(return_value=True)
        ) as mock:
            self.assertEqual(
                {
                    self.initial_admin_status,
                    self.initial_division_member_status,
                    self.initial_admin_division_member_status
                },
                set(get_initial_statuses(self.superuser, self.period))
            )
            mock.assert_called_once_with(self.superuser, self.period)

    def test_get_new_statuses(self) -> None:
        """Тестирование функции `get_new_statuses`."""
        self.assertEqual(
            [self.new_statuses[3]],
            get_new_statuses(self.superuser, self.document)
        )

    def test_add_document_status(self) -> None:
        """Тестирование функции `add_document_status`."""
        with patch.object(
            self.superuser, 'has_perm', new=lambda perm: perm != 'dcis.change_document'
        ), self.assertRaises(PermissionDenied):
            self._add_document_status()
        with patch(
            'apps.dcis.services.status_services.AddStatusActions.TestAction',
            create=True,
            new=self.TestAction
        ):
            actual_document_status = self._add_document_status()
            self.TestAction.pre_mock.assert_called_once_with(self.add_document)
            self.TestAction.post_mock.assert_called_once_with(self.add_document, actual_document_status)
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


class CheckLimitationsTestCase(TestCase):
    """Тестирование класса `CheckLimitations`."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""

        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)

        self.sheet1 = Sheet.objects.create(period=self.period, name='sheet1')
        self.sheet1_columns = [ColumnDimension.objects.create(index=i, sheet=self.sheet1) for i in range(1, 4)]
        self.sheet1_row = RowDimension.objects.create(index=1, sheet=self.sheet1)
        self.sheet1_cells = {
            'A1': Cell.objects.create(column=self.sheet1_columns[0], row=self.sheet1_row, kind='n'),
            'B1': Cell.objects.create(column=self.sheet1_columns[1], row=self.sheet1_row, kind='n'),
            'C1': Cell.objects.create(formula='=A1+B1', column=self.sheet1_columns[2], row=self.sheet1_row, kind='n'),
        }

        self.sheet2 = Sheet.objects.create(period=self.period, name='sheet2')
        self.sheet2_column = ColumnDimension.objects.create(index=1, sheet=self.sheet2)
        self.sheet2_rows = [RowDimension.objects.create(index=i, sheet=self.sheet2) for i in range(1, 3)]
        self.sheet2_cells = {
            'A1': Cell.objects.create(
                formula='=sheet1!A1',
                column=self.sheet2_column,
                row=self.sheet2_rows[0], kind='n'
            ),
            'A2': Cell.objects.create(column=self.sheet2_column, row=self.sheet2_rows[1], kind='n'),
        }

        self.sheet3 = Sheet.objects.create(period=self.period, name='sheet3')
        self.sheet3_columns = [ColumnDimension.objects.create(index=i, sheet=self.sheet3) for i in range(1, 3)]
        self.sheet3_rows = [RowDimension.objects.create(index=i, sheet=self.sheet3) for i in range(1, 3)]
        self.sheet3_cells = {
            'A1': Cell.objects.create(column=self.sheet3_columns[0], row=self.sheet3_rows[0], kind='n'),
            'B1': Cell.objects.create(column=self.sheet3_columns[1], row=self.sheet3_rows[0], kind='n'),
            'A2': Cell.objects.create(column=self.sheet3_columns[0], row=self.sheet3_rows[1], kind='n'),
            'B2': Cell.objects.create(column=self.sheet3_columns[1], row=self.sheet3_rows[1], kind='n'),
        }

        self.limitations = [
            Limitation.objects.create(
                index=1,
                formula='sheet1!C1 > 5',
                error_message='sheet1!C1 больше 5',
                sheet=self.sheet1,
            ),
            Limitation.objects.create(
                index=2,
                formula='2 / sheet2!A1 > 0.2',
                error_message='sheet2!A1 больше 0.2',
                sheet=self.sheet2,
            ),
            Limitation.objects.create(
                index=3,
                formula='sheet2!A2 < sheet1!C1',
                error_message='sheet2!A2 меньше sheet1!C1',
                sheet=self.sheet2,
            ),
            Limitation.objects.create(
                index=4,
                formula='SUM(sheet3!A1:B2) > 10',
                error_message='SUM(sheet3!A1:B2) меньше или равно 10',
                sheet=self.sheet3,
            )
        ]

        self.document_with_calculation_errors = self._create_document(['0', '6', '6'], ['0', '3'], ['2', '4', '2', '4'])
        self.document_with_limitation_errors = self._create_document(['1', '2', '3'], ['1', '4'], ['2', '3', '2', '3'])
        self.document_without_errors = self._create_document(['3', '4', '7'], ['3', '5'], ['2', '4', '2', '4'])

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
    def test_check_limitations_with_calculation_errors(self) -> None:
        """Тестирование функции `check_limitations` с ошибками вычислений."""
        with self.assertRaises(ValidationError) as error:
            AddStatusActions.CheckLimitations.pre_execute(self.document_with_calculation_errors)
        self.assertEqual(
            [
                LimitationError(
                    form='sheet2',
                    formula='2 / sheet2!A1 > 0.2',
                    error_message='Деление на 0',
                    dependencies=encode({'sheet2!A1': 0.0})
                )
            ],
            error.exception.params,
        )

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
    def test_check_limitations_with_limitation_errors(self) -> None:
        """Тестирование функции `check_limitations` с ошибками ограничений."""
        with self.assertRaises(ValidationError) as error:
            AddStatusActions.CheckLimitations.pre_execute(self.document_with_limitation_errors)
        self.assertEqual(
            [
                LimitationError(
                    form='sheet1',
                    formula='sheet1!C1 > 5',
                    error_message='sheet1!C1 больше 5',
                    dependencies=encode({'sheet1!C1': 3.0}),
                ),
                LimitationError(
                    form='sheet2',
                    formula='sheet2!A2 < sheet1!C1',
                    error_message='sheet2!A2 меньше sheet1!C1',
                    dependencies=encode({
                        'sheet2!A2': 4.0,
                        'sheet1!C1': 3.0,
                    }),
                ),
                LimitationError(
                    form='sheet3',
                    formula='SUM(sheet3!A1:B2) > 10',
                    error_message='SUM(sheet3!A1:B2) меньше или равно 10',
                    dependencies=encode({
                        'sheet3!A1': 2.0,
                        'sheet3!B1': 3.0,
                        'sheet3!A2': 2.0,
                        'sheet3!B2': 3.0,
                    }),
                ),
            ],
            error.exception.params,
        )

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
    def test_check_limitations(self) -> None:
        """Тестирование функции `check_limitations` без ошибок."""
        AddStatusActions.CheckLimitations.pre_execute(self.document_without_errors)

    def _create_document(
        self,
        sheet1_values: list[str],
        sheet2_values: list[str],
        sheet3_values: list[str],
    ) -> Document:
        """Создание документа со значениями."""
        document = Document.objects.create(period=self.period)
        document.sheets.set([self.sheet1, self.sheet2, self.sheet3])
        for value, column in zip(sheet1_values, self.sheet1_columns):
            Value.objects.create(
                value=value,
                document=document,
                sheet=self.sheet1,
                column=column,
                row=self.sheet1_row,
            )
        for value, row in zip(sheet2_values, self.sheet2_rows):
            Value.objects.create(
                value=value,
                document=document,
                sheet=self.sheet2,
                column=self.sheet2_column,
                row=row,
            )
        for value, dimensions in zip(sheet3_values, product(self.sheet3_rows, self.sheet3_columns)):
            Value.objects.create(
                value=value,
                document=document,
                sheet=self.sheet3,
                column=dimensions[1],
                row=dimensions[0],
            )
        return document


class ArchivePeriodTestCase(TestCase):
    """Тестирование класса `ArchivePeriod`."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""

        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.department_content_type = ContentType.objects.get_for_model(Department)
        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)
        self.document = Document.objects.create(period=self.period)
        self.status = Status.objects.create(name='new_status')
        self.document_status = DocumentStatus.objects.create(
            document=self.document,
            status=self.status,
            user_id=self.user.id
        )

        self.sheet = Sheet.objects.create(period=self.period, name='sheet1')
        self.sheet_columns = [ColumnDimension.objects.create(index=i, sheet=self.sheet) for i in range(1, 4)]
        self.sheet_row1 = RowDimension.objects.create(index=1, sheet=self.sheet)
        self.sheet_row2 = RowDimension.objects.create(index=2, sheet=self.sheet)
        self.sheet_row3 = RowDimension.objects.create(
            dynamic=False,
            index=1,
            parent_id=self.sheet_row1.id,
            sheet=self.sheet,
            fixed=True,
            hidden=True
        )
        self.sheet_row4 = RowDimension.objects.create(index=1, parent_id=self.sheet_row3.id, sheet=self.sheet)
        self.sheet_row5 = RowDimension.objects.create(index=2, parent_id=self.sheet_row1.id, sheet=self.sheet)

    def test_archive_period(self) -> None:
        """Тестирование функции архивирования периода"""

        AddStatusActions.ArchivePeriod.post_execute(self.document, self.document_status)
        archive_period = self.document_status.archive_period
        archive_document = archive_period.document_set.all().first()
        test_rows = self.document.rowdimension_set.filter(parent_id__isnull=False).order_by('id').all()
        archive_rows = archive_document.rowdimension_set.filter(parent_id__isnull=False).order_by('id').all()
        for test_row, archive_row in zip(test_rows, archive_rows):
            self.assertEqual(test_row.height, archive_row.height)
            self.assertEqual(test_row.dynamic, archive_row.dynamic)
            self.assertEqual(test_row.index, archive_row.index)
            self.assertEqual(test_row.fixed, archive_row.fixed)
            self.assertEqual(test_row.hidden, archive_row.hidden)
