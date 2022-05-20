from typing import Any, Optional

import graphene
from devind_core.schema import FileType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.db.models import F
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import Cell, Document, RowDimension, Sheet, Value
from apps.dcis.schema.types import CellType, RowDimensionType
from apps.dcis.services.cell_services import change_cell_kind, check_cell_options
from apps.dcis.services.sheet_services import add_row, move_merged_cells
from apps.dcis.services.value_services import (
    create_file_value_archive,
    get_file_value_files,
    update_or_create_file_value,
    update_or_create_value,
    updates_values_by_cell_kind_change,
)


class AddRowDimensionMutation(BaseMutation):
    """Добавление строки."""

    class Input:
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')
        document_id = graphene.ID(description='Идентификатор документа')
        parent_id = graphene.ID(description='Идентификатор родительской строки')
        index = graphene.Int(required=True, description='Индекс вставки')

    row_dimension = graphene.Field(RowDimensionType, required=True, description='Добавленная строка')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        document_id: Optional[str],
        sheet_id: int,
        parent_id: Optional[str],
        index: int
    ):
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        sheet: Sheet = get_object_or_404(Sheet, pk=sheet_id)
        row_dimension = add_row(info.context.user, sheet, document, int(parent_id) if parent_id else None, index)
        return AddRowDimensionMutation(row_dimension=row_dimension)


class DeleteRowDimensionMutation(BaseMutation):
    """Удаление строки."""

    class Input:
        row_id = graphene.Int(required=True, description='Идентификатор строки')

    row_id = graphene.Int(required=True, description='Идентификатор удаленной строки')
    index = graphene.Int(required=True, description='Измененные строки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, row_id: int):
        row: RowDimension = get_object_or_404(RowDimension, pk=row_id)
        sheet: Sheet = Sheet.objects.get(pk=row.sheet_id)
        row.delete()
        sheet.rowdimension_set.filter(index__gt=row.index).update(index=F('index') - 1)
        move_merged_cells(sheet, row.index, -1, True)
        return DeleteRowDimensionMutation(row_id=row_id, index=row.index, merged_cells=sheet.mergedcell_set.all())


class ChangeCellsOptionMutation(BaseMutation):
    """Изменение свойств ячеек:

        - horizontal_align - ['left', 'center', 'right']
        - vertical_align - ['top', 'middle', 'bottom']
        - size - цифра от 10 до 24
        - strong - true, false
        - italic - true, false
        - underline - [None, 'single', 'double', 'single_accounting', 'double_accounting']
        - kind - [
            'n', 's', 'f', 'b', 'inlineStr', 'e', 'str', 'd', 'text', 'money',
            'bigMoney', 'fl', 'user', 'department', 'organization', 'classification'
        ]
    """

    class Input:
        cells_id = graphene.List(graphene.NonNull(graphene.Int), required=True, description='Идентификатор ячейки')
        field = graphene.String(required=True, description='Идентификатор поля')
        value = graphene.String(description='Значение поля')

    cells = graphene.List(CellType, description='Измененные ячейки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        cells_id: list[int],
        field: str,
        value: Optional[str] = None
    ):
        success, value, errors = check_cell_options(field, value)
        if not success:
            return ChangeCellsOptionMutation(success=success, errors=errors)
        cells = Cell.objects.filter(pk__in=cells_id).all()
        values: list[Value] = []
        with transaction.atomic():
            for cell in cells:
                if field == 'kind':
                    cell.save(update_fields=change_cell_kind(cell, value))
                    values.extend(updates_values_by_cell_kind_change(cell))
                else:
                    setattr(cell, field, value)
                    cell.save(update_fields=(field,))
        return ChangeCellsOptionMutation(cells=cells, values=values)


class UnloadFileValueArchiveMutation(BaseMutation):
    """Выгрузка архива значения ячейки типа `Файл`."""

    class Input:
        value_id = graphene.ID(required=True, description='Идентификатор значения ячейки')

    src = graphene.String(description='Ссылка на сгенерированный архив')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, value_id: str):
        return UnloadFileValueArchiveMutation(src=create_file_value_archive(get_object_or_404(Value, pk=value_id)))


class ChangeValueMutation(BaseMutation):
    """Изменение значения ячейки."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        sheet_id = graphene.Int(required=True, description='Идентификатор листа')
        column_id = graphene.Int(required=True, description='Идентификатор колонки')
        row_id = graphene.Int(required=True, description='Идентификатор строки')
        value = graphene.String(required=True, description='Значение')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: None,
        info: ResolveInfo,
        document_id: str,
        sheet_id: int,
        column_id: int,
        row_id: int,
        value: str
    ):
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        sheet: Sheet = get_object_or_404(Sheet, pk=sheet_id)
        val, _ = update_or_create_value(
            document=document,
            sheet=sheet,
            column_id=column_id,
            row_id=row_id,
            value=value
        )
        return ChangeValueMutation(value=val)


class ChangeFileValueMutation(BaseMutation):
    """Изменение значения ячейки типа `Файл`."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        sheet_id = graphene.Int(required=True, description='Идентификатор листа')
        column_id = graphene.Int(required=True, description='Идентификатор колонки')
        row_id = graphene.Int(required=True, description='Идентификатор строки')
        value = graphene.String(required=True, description='Значение')
        remaining_files = graphene.List(graphene.NonNull(graphene.ID), required=True, description='Оставшиеся файлы')
        new_files = graphene.List(graphene.NonNull(Upload), required=True, description='Новые файлы')

    value_files = graphene.List(FileType, description='Измененные файлы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: None,
        info: ResolveInfo,
        document_id: str,
        sheet_id: int,
        column_id: int,
        row_id: int,
        value: str,
        remaining_files: list[int],
        new_files: list[InMemoryUploadedFile]
    ):
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        sheet: Sheet = get_object_or_404(Sheet, pk=sheet_id)
        val, _ = update_or_create_file_value(
            user=info.context.user,
            document=document,
            sheet=sheet,
            column_id=column_id,
            row_id=row_id,
            value=value,
            remaining_files=[int(from_global_id(global_id)[1]) for global_id in remaining_files],
            new_files=new_files
        )
        return ChangeFileValueMutation(value=val, value_files=get_file_value_files(val))


class SheetMutations(graphene.ObjectType):
    """Список мутаций для работы с листами документа."""

    add_row_dimension = AddRowDimensionMutation.Field(required=True, description='Добавление строки')
    delete_row_dimension = DeleteRowDimensionMutation.Field(required=True, description='Удаление строки')

    change_cells_option = ChangeCellsOptionMutation.Field(required=True, description='Изменения опций ячейки')

    unload_file_value_archive = UnloadFileValueArchiveMutation.Field(
        required=True,
        description='Выгрузка архива значения ячейки типа `Файл`'
    )
    change_value = ChangeValueMutation.Field(required=True, description='Изменение значения ячейки')
    change_file_value = ChangeFileValueMutation.Field(
        required=True,
        description='Изменение значения ячейки типа `Файл`'
    )
