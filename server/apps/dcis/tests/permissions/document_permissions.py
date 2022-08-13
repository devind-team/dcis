"""Тесты разрешений на работу с документами периодов."""

from typing import Callable
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied

from apps.dcis.models import Cell, ColumnDimension, Document, Period, Project, RowDimension, Sheet, Status
from apps.dcis.permissions.document_permissions import (
    can_add_child_row_dimension,
    can_add_document,
    can_add_document_status,
    can_change_child_row_dimension_height,
    can_change_document,
    can_change_document_comment,
    can_change_value,
    can_delete_child_row_dimension,
    can_view_document,
)
from .common import PermissionsTestCase


class DocumentPermissionsTestCase(PermissionsTestCase):
    """Тесты разрешений на работу с документами периодов."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        super().setUp()

        self.department_content_type = ContentType.objects.get_for_model(Department)

        self.status_edit = Status.objects.create(edit=True, protected=False)
        self.protected_status_edit = Status.objects.create(edit=True, protected=True)

        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)
        self.document = Document.objects.create(period=self.period)
        self.document.documentstatus_set.create(
            document=self.document,
            status=self.status_edit,
            user=self.user
        )

        self.user_project = Project.objects.create(user=self.user, content_type=self.department_content_type)
        self.user_period = Period.objects.create(user=self.user, project=self.user_project)
        self.sheet = Sheet.objects.create(period=self.user_period)
        self.row_dimension = RowDimension.objects.create(index=1, sheet=self.sheet)
        self.column_dimensions = [
            ColumnDimension.objects.create(index=i, sheet=self.sheet) for i in range(1, 7)
        ]

        self.user_document = Document.objects.create(user=self.user, period=self.user_period)
        self.user_document.documentstatus_set.create(
            document=self.user_document,
            status=self.status_edit,
            user=self.user
        )

        self.user_period_document = Document.objects.create(period=self.user_period)
        self.user_period_document.documentstatus_set.create(
            document=self.user_period_document,
            status=self.status_edit,
            user=self.user
        )

        self.document_row_dimension = RowDimension.objects.create(
            index=1,
            sheet=self.sheet,
            document=self.user_period_document,
            parent=self.row_dimension,
        )
        self.user_document_row_dimension = RowDimension.objects.create(
            index=1,
            sheet=self.sheet,
            document=self.user_document,
            parent=self.row_dimension,
            dynamic=True,
        )
        self.user_period_document_row_dimension = RowDimension.objects.create(
            index=2,
            sheet=self.sheet,
            document=self.user_period_document,
            parent=self.row_dimension,
            user=self.user,
        )
        self.document_row_dimension_with_child = RowDimension.objects.create(
            index=3,
            sheet=self.sheet,
            document=self.user_period_document,
            parent=self.row_dimension,
        )
        self.document_row_dimension_child = RowDimension.objects.create(
            index=1,
            sheet=self.sheet,
            document=self.user_period_document,
            parent=self.document_row_dimension_with_child,
        )
        self.dynamic_row_dimension = RowDimension.objects.create(index=2, sheet=self.sheet, dynamic=True)
        self.document_dynamic_row_dimension = RowDimension.objects.create(
            index=1,
            sheet=self.sheet,
            document=self.user_period_document,
            parent=self.dynamic_row_dimension,
            dynamic=True,
        )

        self.not_editable_cell_obj = {
            'document': self.user_period_document,
            'cell': Cell.objects.create(
                row=self.row_dimension,
                column=self.column_dimensions[0],
                editable=False,
            ),
        }
        self.formula_cell_obj = {
            'document': self.user_period_document,
            'cell': Cell.objects.create(
                row=self.row_dimension,
                column=self.column_dimensions[1],
                formula='0',
            ),
        }
        self.cell_obj = {
            'document': self.document,
            'cell': Cell.objects.create(row=self.row_dimension, column=self.column_dimensions[2]),
        }
        self.child_cell_obj = {
            'document': self.user_period_document,
            'cell': Cell.objects.create(row=self.document_row_dimension_child, column=self.column_dimensions[3])
        }
        self.user_period_cell_obj = {
            'document': self.user_period_document,
            'cell': Cell.objects.create(row=self.row_dimension, column=self.column_dimensions[4]),
        }
        self.user_document_cell_obj = {
            'document': self.user_document,
            'cell': Cell.objects.create(row=self.row_dimension, column=self.column_dimensions[5])
        }

    def test_can_view_document(self) -> None:
        """Тестирование функции `can_view_document`."""
        self.assertRaises(PermissionDenied, can_view_document, self.user, self.document)
        with patch.object(self.user, 'has_perm', new=lambda perm: perm in ('dcis.view_project', 'dcis.view_period')):
            self.assertRaises(PermissionDenied, can_view_document, self.user, self.document)
        can_view_document(self.user, self.user_period_document)

    def test_can_add_document(self) -> None:
        """Тестирование функции `can_add_document`."""
        self.assertRaises(PermissionDenied, can_add_document, self.user, self.period, self.status_edit, 1)
        with patch.object(
            self.user,
            'has_perm',
            new=lambda perm: perm in ('dcis.view_project', 'dcis.view_period')
        ), patch(
            'apps.dcis.permissions.document_permissions.get_user_divisions',
            new=Mock(return_value=({'id': 1},))
        ), patch.object(
            self.period, 'multiple', new=True,
        ):
            can_add_document(self.user, self.period, self.status_edit, 1)
            self.assertRaises(PermissionDenied, can_add_document, self.user, self.period, self.protected_status_edit, 1)
            self.assertRaises(PermissionDenied, can_add_document, self.user, self.period, self.status_edit, 2)
        with patch.object(self.user, 'has_perm', new=lambda perm: perm in ('dcis.view_project', 'dcis.view_period')):
            self.assertRaises(PermissionDenied, can_add_document, self.user, self.period, self.status_edit, 1)
        with patch.object(
            self.user,
            'has_perm',
            new=lambda perm: perm in ('dcis.view_project', 'dcis.view_period', 'dcis.add_document')
        ):
            can_add_document(self.user, self.period, self.status_edit, 1)
        self.assertRaises(PermissionDenied, can_add_document, self.user, self.user_period, self.status_edit, 1)
        for global_perm in ('dcis.add_project', 'dcis.add_period'):
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == global_perm):
                self.assertRaises(PermissionDenied, can_add_document, self.user, self.period, self.status_edit, 1)
                can_add_document(self.user, self.user_period, self.status_edit, 1)

    def test_can_change_document(self) -> None:
        """Тестирование функции `can_change_document`."""
        self._test_common(can_change_document)

    def test_can_change_document_comment(self) -> None:
        """Тестирование функции `can_change_document_comment`."""
        self._test_common(can_change_document_comment)
        can_change_document_comment(self.user, self.user_document)

    def test_can_add_document_status(self) -> None:
        """Тестирование функции `can_add_document_status`."""
        self._test_common(can_add_document_status, self.status_edit)
        can_add_document_status(self.user, self.user_document, self.status_edit)
        self.assertRaises(
            PermissionDenied,
            can_add_document_status,
            self.user,
            self.user_document,
            self.protected_status_edit
        )

    def test_can_change_value(self) -> None:
        """Тестирование функции `can_change_value`."""
        with patch(
            'apps.dcis.permissions.document_permissions.ChangeDocumentSheetBase.is_document_editable',
            new=Mock(__bool__=lambda _: False)
        ):
            self._test_can_change_value((False, False, False, False, False, False))
        self._test_can_change_value((False, False, False, False, True, True))
        with patch(
            'apps.dcis.permissions.document_permissions.can_view_document',
            new=Mock(side_effect=PermissionDenied())
        ):
            self._test_can_change_value((False, False, False, False, False, False))
        with patch(
            'apps.dcis.permissions.document_permissions.can_view_document',
            new=Mock()
        ):
            self._test_can_change_value((False, False, True, False, True, True))
            with patch(
                'apps.dcis.permissions.document_permissions.can_change_period_sheet_base',
                new=Mock(return_value=True)
            ):
                self._test_can_change_value((False, False, True, True, True, True))
            with patch.object(self.user, 'has_perm', lambda perm: perm == 'dcis.change_value'):
                self._test_can_change_value((False, False, True, True, True, True))
            with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
                self._test_can_change_value((False, False, True, True, True, True))
                mock.assert_called_with(self.user.id, self.user_period.id, 'change_value')
            with patch(
                'apps.dcis.permissions.document_permissions.get_user_divisions',
                new=Mock(return_value=({'id': 1},))
            ) as mock:
                self._test_can_change_value((False, False, True, False, True, True))
                with patch.object(self.user_period_document, 'object_id', new=1), patch.object(
                    self.user_period, 'multiple', new=True,
                ):
                    self._test_can_change_value((False, False, True, True, True, True))
                    mock.assert_called_with(self.user, self.user_project)
                with patch.object(self.document_row_dimension_child, 'object_id', new=1):
                    self._test_can_change_value((False, False, True, True, True, True))

    def test_can_add_child_row_dimension(self) -> None:
        """Тестирование функции `can_add_child_row_dimension`."""
        with patch(
            'apps.dcis.permissions.document_permissions.ChangeDocumentSheetBase.is_document_editable',
            new=Mock(__bool__=lambda _: False)
        ):
            self._test_can_add_child_row_dimension((False, False, False, False, False))
        self._test_can_add_child_row_dimension((False, False, True, False, True))
        with patch.object(self.user, 'has_perm', lambda perm: perm == 'dcis.change_sheet'):
            self._test_can_add_child_row_dimension((False, False, True, True, True))
        with patch.object(self.user, 'has_perm', lambda perm: perm == 'dcis.add_rowdimension'):
            self._test_can_add_child_row_dimension((False, False, True, True, True))
        with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
            self._test_can_add_child_row_dimension((False, False, True, True, True))
            mock.assert_called_with(self.user.id, self.user_period.id, 'add_rowdimension')
        with patch(
            'apps.dcis.permissions.document_permissions.get_user_divisions',
            new=Mock(return_value=({'id': 1},))
        ) as mock:
            self._test_can_add_child_row_dimension((False, False, True, False, True))
            with patch.object(self.user_period_document, 'object_id', new=1), patch.object(
                self.user_period, 'multiple', new=True,
            ):
                self._test_can_add_child_row_dimension((False, False, True, True, True))
            with patch.object(self.document_dynamic_row_dimension, 'object_id', new=1):
                self._test_can_add_child_row_dimension((False, False, True, True, True))

    def test_can_change_child_row_dimension_height(self) -> None:
        """Тестирование функции `can_change_child_row_dimension_height`."""
        with patch(
            'apps.dcis.permissions.document_permissions.ChangeDocumentSheetBase.is_document_editable',
            new=Mock(__bool__=lambda _: False)
        ):
            self._test_can_change_child_row_dimension_height((False, False, False, False))
        self._test_can_change_child_row_dimension_height((False, False, True, True))
        with patch.object(self.user, 'has_perm', lambda perm: perm == 'dcis.change_sheet'):
            self._test_can_change_child_row_dimension_height((False, True, True, True))
        with patch.object(self.user, 'has_perm', lambda perm: perm == 'dcis.change_rowdimension'):
            self._test_can_change_child_row_dimension_height((False, True, True, True))
        with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
            self._test_can_change_child_row_dimension_height((False, True, True, True))
            mock.assert_called_with(self.user.id, self.user_period.id, 'change_rowdimension')

    def test_can_delete_child_row_dimension(self) -> None:
        """Тестирование функции `can_delete_child_row_dimension`."""
        with patch(
            'apps.dcis.permissions.document_permissions.ChangeDocumentSheetBase.is_document_editable',
            new=Mock(__bool__=lambda _: False)
        ):
            self._test_can_delete_child_row_dimension((False, False, False, False, False))
        self._test_can_delete_child_row_dimension((False, False, False, True, True))
        with patch.object(self.user, 'has_perm', lambda perm: perm == 'dcis.change_sheet'):
            self._test_can_delete_child_row_dimension((False, False, True, True, True))
        with patch.object(self.user, 'has_perm', lambda perm: perm == 'dcis.delete_rowdimension'):
            self._test_can_delete_child_row_dimension((False, False, True, True, True))
        with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
            self._test_can_delete_child_row_dimension((False, False, True, True, True))
            mock.assert_called_with(self.user.id, self.user_period.id, 'delete_rowdimension')

    def _test_common(self, f: Callable, *args) -> None:
        """Общий механизм тестирования для функций проверки разрешений на изменение документа."""
        self.assertRaises(PermissionDenied, f, self.user, self.document, *args)
        self.assertRaises(PermissionDenied, f, self.user, self.user_period_document, *args)
        with patch(
            'apps.dcis.permissions.document_permissions.can_view_document',
            new=Mock()
        ):
            self.assertRaises(PermissionDenied, f, self.user, self.document, *args)
            self.assertRaises(PermissionDenied, f, self.user, self.user_period_document, *args)
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == 'dcis.change_document'):
                f(self.user, self.document, *args)
                f(self.user, self.user_period_document, *args)
            for global_perm in ('dcis.add_project', 'dcis.add_period'):
                with patch.object(self.user, 'has_perm', new=lambda perm: perm == global_perm):
                    self.assertRaises(PermissionDenied, f, self.user, self.document, *args)
                    f(self.user, self.user_period_document, *args)
            with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
                f(self.user, self.document, *args)
                mock.assert_called_once_with(self.user.id, self.period.id, 'change_document')
            with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
                f(self.user, self.user_period_document, *args)
                mock.assert_called_once_with(self.user.id, self.user_period.id, 'change_document')

    def _test_can_change_value(self, values: tuple[bool, bool, bool, bool, bool, bool]) -> None:
        """Тестирование функции `can_change_value` для 6 типов ячеек."""
        for cell_obj, value in zip((
            self.not_editable_cell_obj,
            self.formula_cell_obj,
            self.cell_obj,
            self.child_cell_obj,
            self.user_period_cell_obj,
            self.user_document_cell_obj,
        ), values):
            if value:
                can_change_value(self.user, cell_obj['document'], cell_obj['cell'])
            else:
                self.assertRaises(
                    PermissionDenied,
                    can_change_value,
                    self.user,
                    cell_obj['document'],
                    cell_obj['cell']
                )

    def _test_can_add_child_row_dimension(self, values: tuple[bool, bool, bool, bool, bool]) -> None:
        """Тестирование функции `can_add_child_row_dimension` для 5 типов строк."""
        for row_dimension, value in zip((
            {'document': self.user_period_document, 'row_dimension': self.row_dimension},
            {'document': self.user_period_document, 'row_dimension': self.document_row_dimension},
            {'document': self.user_period_document, 'row_dimension': self.dynamic_row_dimension},
            {'document': self.user_period_document, 'row_dimension': self.document_dynamic_row_dimension},
            {'document': self.user_document, 'row_dimension': self.user_document_row_dimension},
        ), values):
            if value:
                can_add_child_row_dimension(
                    self.user,
                    row_dimension['document'],
                    row_dimension['row_dimension']
                )
            else:
                self.assertRaises(
                    PermissionDenied,
                    can_add_child_row_dimension,
                    self.user,
                    row_dimension['document'],
                    row_dimension['row_dimension']
                )

    def _test_can_change_child_row_dimension_height(self, values: tuple[bool, bool, bool, bool]) -> None:
        """Тестирование функции `can_change_child_row_dimension_height` для 4 типов строк."""
        for row_dimension, value in zip((
            self.row_dimension,
            self.document_row_dimension,
            self.user_period_document_row_dimension,
            self.user_document_row_dimension,
        ), values):
            if value:
                can_change_child_row_dimension_height(self.user, row_dimension)
            else:
                self.assertRaises(
                    PermissionDenied,
                    can_change_child_row_dimension_height,
                    self.user,
                    row_dimension
                )

    def _test_can_delete_child_row_dimension(self, values: tuple[bool, bool, bool, bool, bool]) -> None:
        """Тестирование функции `can_delete_child_row_dimension` для 5 типов строк."""
        for row_dimension, value in zip((
            self.row_dimension,
            self.document_row_dimension_with_child,
            self.document_row_dimension,
            self.user_period_document_row_dimension,
            self.user_document_row_dimension,
        ), values):
            if value:
                can_delete_child_row_dimension(self.user, row_dimension)
            else:
                self.assertRaises(PermissionDenied, can_delete_child_row_dimension, self.user, row_dimension)
