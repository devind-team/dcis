"""Тесты разрешений на работу с документами периодов."""

from typing import Type
from unittest.mock import Mock, patch

from devind_dictionaries.models import Department
from devind_helpers.permissions import BasePermission
from django.contrib.contenttypes.models import ContentType

from apps.dcis.models import Cell, ColumnDimension, Document, Period, Project, RowDimension, Sheet
from apps.dcis.permissions.document_permissions import (
    AddChildRowDimension,
    AddDocument,
    ChangeDocument,
    ChangeValue,
    ChangeValueBase,
    DeleteChildRowDimension,
    DeleteDocument,
    ViewDocument,
)
from .common import PermissionsTestCase


class DocumentPermissionsTestCase(PermissionsTestCase):
    """Тесты разрешений на работу с документами периодов."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        super().setUp()

        self.department_content_type = ContentType.objects.get_for_model(Department)

        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)
        self.document = Document.objects.create(period=self.period)

        self.user_project = Project.objects.create(user=self.user, content_type=self.department_content_type)
        self.user_period = Period.objects.create(user=self.user, project=self.user_project)
        self.user_document = Document.objects.create(period=self.user_period)

        self.sheet = Sheet.objects.create(period=self.user_period)
        self.row_dimension = RowDimension.objects.create(index=1, sheet=self.sheet)
        self.document_row_dimension = RowDimension.objects.create(
            index=2,
            sheet=self.sheet,
            document=self.user_document,
        )
        self.document_user_row_dimension = RowDimension.objects.create(
            index=3,
            sheet=self.sheet,
            document=self.user_document,
            user=self.user,
        )
        self.document_row_dimension_with_child = RowDimension.objects.create(
            index=4,
            sheet=self.sheet,
            document=self.user_document,
        )
        self.document_row_dimension_child = RowDimension.objects.create(
            index=1,
            sheet=self.sheet,
            document=self.user_document,
            parent=self.document_row_dimension_with_child,
        )
        self.dynamic_row_dimension = RowDimension.objects.create(index=5, sheet=self.sheet, dynamic=True)
        self.document_dynamic_row_dimension = RowDimension.objects.create(
            index=6,
            sheet=self.sheet,
            document=self.user_document,
            dynamic=True,
        )
        self.column_dimensions = [ColumnDimension.objects.create(index=i, sheet=self.sheet) for i in range(1, 6)]
        self.not_editable_cell_obj = ChangeValueBase.Obj(
            document=self.user_document,
            cell=Cell.objects.create(
                row=self.row_dimension,
                column=self.column_dimensions[0],
                editable=False,
            ),
        )
        self.formula_cell_obj = ChangeValueBase.Obj(
            document=self.user_document,
            cell=Cell.objects.create(
                row=self.row_dimension,
                column=self.column_dimensions[1],
                formula='0',
            ),
        )
        self.cell_obj = ChangeValueBase.Obj(
            document=self.document,
            cell=Cell.objects.create(row=self.row_dimension, column=self.column_dimensions[2]),
        )
        self.child_cell_obj = ChangeValueBase.Obj(
            document=self.user_document,
            cell=Cell.objects.create(row=self.document_row_dimension_child, column=self.column_dimensions[3])
        )
        self.user_cell_obj = ChangeValueBase.Obj(
            document=self.user_document,
            cell=Cell.objects.create(row=self.row_dimension, column=self.column_dimensions[4]),
        )

    def test_view_document(self) -> None:
        """Тестирование класса `ViewDocument`."""
        self.assertFalse(ViewDocument.has_object_permission(self.context_mock, self.document))
        with patch.object(self.user, 'has_perm', new=lambda perm: perm in ('dcis.view_project', 'dcis.view_period')):
            self.assertFalse(ViewDocument.has_object_permission(self.context_mock, self.document))
        self.assertTrue(ViewDocument.has_object_permission(self.context_mock, self.user_document))

    def test_add_document(self) -> None:
        """Тестирование класса `AddDocument`."""
        self.assertFalse(AddDocument.has_object_permission(self.context_mock, self.period))
        with patch.object(self.user, 'has_perm', new=lambda perm: perm in ('dcis.view_project', 'dcis.view_period')):
            self.assertFalse(AddDocument.has_object_permission(self.context_mock, self.period))
        with patch.object(
            self.user,
            'has_perm',
            new=lambda perm: perm in ('dcis.view_project', 'dcis.view_period', 'dcis.add_document')
        ):
            self.assertTrue(AddDocument.has_object_permission(self.context_mock, self.period))
        self.assertFalse(AddDocument.has_object_permission(self.context_mock, self.user_period))
        for global_perm in ('dcis.add_project', 'dcis.add_period'):
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == global_perm):
                self.assertFalse(AddDocument.has_object_permission(self.context_mock, self.period))
                self.assertTrue(AddDocument.has_object_permission(self.context_mock, self.user_period))

    def test_change_document(self) -> None:
        """Тестирование класса `ChangeDocument`."""
        self._test_common(ChangeDocument, 'dcis.change_document', 'change_document')

    def test_delete_document(self) -> None:
        """Тестирование класса `DeleteDocument`."""
        self._test_common(DeleteDocument, 'dcis.delete_document', 'delete_document')

    def test_change_value(self) -> None:
        """Тестирование класса `ChangeValue`."""
        self._test_change_value((False, False, False, False, True))
        with patch(
            'apps.dcis.permissions.document_permissions.ViewDocument.has_object_permission',
            new=Mock(return_value=False)
        ):
            self._test_change_value((False, False, False, False, False))
        with patch(
            'apps.dcis.permissions.document_permissions.ViewDocument.has_object_permission',
            new=Mock(return_value=True)
        ):
            self._test_change_value((False, False, True, False, True))
            with patch(
                'apps.dcis.permissions.document_permissions.ChangePeriodSheet.has_object_permission',
                new=Mock(return_value=True)
            ):
                self._test_change_value((False, False, True, True, True))
            with patch.object(self.user, 'has_perm', lambda perm: perm == 'dcis.change_value'):
                self._test_change_value((False, False, True, True, True))
            with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
                self._test_change_value((False, False, True, True, True))
                mock.assert_called_with(self.user.id, self.user_period.id, 'change_value')
            with patch(
                'apps.dcis.permissions.document_permissions.get_user_divisions',
                new=Mock(return_value=({'id': 1},))
            ) as mock:
                self._test_change_value((False, False, True, False, True))
                with patch.object(self.user_document, 'object_id', new=1), patch.object(
                    self.user_period, 'multiple', new=True,
                ):
                    self._test_change_value((False, False, True, True, True))
                    mock.assert_called_with(self.user, self.user_project)
                with patch.object(self.document_row_dimension_child, 'object_id', new=1):
                    self._test_change_value((False, False, True, True, True))

    def test_add_child_row_dimension(self) -> None:
        """Тестирование класса `AddChildRowDimension`."""
        self._test_add_child_row_dimension((False, False, False, False))
        with patch.object(self.user, 'has_perm', lambda perm: perm == 'dcis.change_sheet'):
            self._test_add_child_row_dimension((False, False, False, True))
        with patch.object(self.user, 'has_perm', lambda perm: perm == 'dcis.add_rowdimension'):
            self._test_add_child_row_dimension((False, False, False, True))
        with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
            self._test_add_child_row_dimension((False, False, False, True))
            mock.assert_called_once_with(self.user.id, self.user_period.id, 'add_rowdimension')

    def test_delete_child_row_dimension(self) -> None:
        """Тестирование класса `DeleteChildRowDimension`"""
        self._test_delete_child_row_dimension((False, False, False, True))
        with patch.object(self.user, 'has_perm', lambda perm: perm == 'dcis.change_sheet'):
            self._test_delete_child_row_dimension((False, False, True, True))
        with patch.object(self.user, 'has_perm', lambda perm: perm == 'dcis.delete_rowdimension'):
            self._test_delete_child_row_dimension((False, False, True, True))
        with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
            self._test_delete_child_row_dimension((False, False, True, True))
            mock.assert_called_with(self.user.id, self.user_period.id, 'delete_rowdimension')

    def _test_common(self, cls: Type[BasePermission], permission: str, privilege: str) -> None:
        """Общий механизм тестирования для классов `ChangeDocument` и `DeleteDocument`."""
        self.assertFalse(cls.has_object_permission(self.context_mock, self.document))
        self.assertFalse(cls.has_object_permission(self.context_mock, self.user_document))
        with patch(
            'apps.dcis.permissions.document_permissions.ViewDocument.has_object_permission',
            new=Mock(return_value=True)
        ):
            self.assertFalse(cls.has_object_permission(self.context_mock, self.document))
            self.assertFalse(cls.has_object_permission(self.context_mock, self.user_document))
            with patch.object(self.user, 'has_perm', new=lambda perm: perm == permission):
                self.assertTrue(cls.has_object_permission(self.context_mock, self.document))
                self.assertTrue(cls.has_object_permission(self.context_mock, self.user_document))
            for global_perm in ('dcis.add_project', 'dcis.add_period'):
                with patch.object(self.user, 'has_perm', new=lambda perm: perm == global_perm):
                    self.assertFalse(cls.has_object_permission(self.context_mock, self.document))
                    self.assertTrue(cls.has_object_permission(self.context_mock, self.user_document))
            with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
                self.assertTrue(cls.has_object_permission(self.context_mock, self.document))
                mock.assert_called_once_with(self.user.id, self.period.id, privilege)
            with patch('apps.dcis.permissions.document_permissions.has_privilege', new=Mock(return_value=True)) as mock:
                self.assertTrue(cls.has_object_permission(self.context_mock, self.user_document))
                mock.assert_called_once_with(self.user.id, self.user_period.id, privilege)

    def _test_change_value(self, values: tuple[bool, bool, bool, bool, bool]) -> None:
        """Тестирование класса `ChangeValue` для 5 типов ячеек."""
        for cell_obj, value in zip((
            self.not_editable_cell_obj,
            self.formula_cell_obj,
            self.cell_obj,
            self.child_cell_obj,
            self.user_cell_obj,
        ), values):
            if value:
                self.assertTrue(ChangeValue.has_object_permission(self.context_mock, cell_obj))
            else:
                self.assertFalse(ChangeValue.has_object_permission(self.context_mock, cell_obj))

    def _test_add_child_row_dimension(self, values: tuple[bool, bool, bool, bool]) -> None:
        """Тестирование класса `AddChildRowDimension` для 4 типов строк."""
        for row_dimension, value in zip((
            self.row_dimension,
            self.document_row_dimension,
            self.dynamic_row_dimension,
            self.document_dynamic_row_dimension,
        ), values):
            if value:
                self.assertTrue(AddChildRowDimension.has_object_permission(self.context_mock, row_dimension))
            else:
                self.assertFalse(AddChildRowDimension.has_object_permission(self.context_mock, row_dimension))

    def _test_delete_child_row_dimension(self, values: tuple[bool, bool, bool, bool]) -> None:
        """Тестирование класса `DeleteChildRowDimension` для 4 типов строк."""
        for row_dimension, value in zip((
            self.row_dimension,
            self.document_row_dimension_with_child,
            self.document_row_dimension,
            self.document_user_row_dimension,
        ), values):
            if value:
                self.assertTrue(DeleteChildRowDimension.has_object_permission(self.context_mock, row_dimension))
            else:
                self.assertFalse(DeleteChildRowDimension.has_object_permission(self.context_mock, row_dimension))
