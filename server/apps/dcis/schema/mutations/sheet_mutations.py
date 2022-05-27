from typing import Any, Optional

import graphene
from devind_core.schema import FileType
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.schema.types import ErrorFieldType
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import F
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from graphql_relay import from_global_id
from stringcase import snakecase

from apps.dcis.models import Cell, ColumnDimension, Document, RowDimension, Sheet, Value
from apps.dcis.schema.types import ChangedCellOption, GlobalIndicesInputType, RowDimensionType
from apps.dcis.services.sheet_services import (
    CheckCellOptions,
    add_row_dimension,
    change_cells_option,
    change_column_dimension,
    change_row_dimension,
    create_file_value_archive,
    get_file_value_files,
    move_merged_cells,
    update_or_create_file_value,
    update_or_create_value,
)


class ChangeColumnDimensionMutation(BaseMutation):
    """Изменение колонки."""

    class Input:
        column_dimension_id = graphene.ID(required=True, description='Идентификатор колонки')
        width = graphene.Int(description='Ширина колонки')
        fixed = graphene.Boolean(required=True, description='Фиксация колонки')
        hidden = graphene.Boolean(required=True, description='Скрытие колонки')
        kind = graphene.String(required=True, description='Тип значения')

    column_dimension_id = graphene.ID(required=True, description='Идентификатор колонки')
    width = graphene.Int(description='Ширина колонки')
    fixed = graphene.Boolean(required=True, description='Фиксация колонки')
    hidden = graphene.Boolean(required=True, description='Скрытие колонки')
    kind = graphene.String(required=True, description='Тип значения')
    updated_at = graphene.DateTime(required=True, description='Дата обновления колонки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        column_dimension_id: str,
        width: Optional[int],
        fixed: bool,
        hidden: bool,
        kind: str
    ):
        column_dimension = change_column_dimension(
            get_object_or_404(ColumnDimension, pk=column_dimension_id),
            width=width,
            fixed=fixed,
            hidden=hidden,
            kind=kind
        )
        return ChangeColumnDimensionMutation(
            column_dimension_id=column_dimension.pk,
            width=column_dimension.width,
            fixed=column_dimension.fixed,
            hidden=column_dimension.hidden,
            kind=column_dimension.kind,
            updated_at=column_dimension.updated_at
        )


class AddRowDimensionMutation(BaseMutation):
    """Добавление строки."""

    class Input:
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')
        document_id = graphene.ID(description='Идентификатор документа')
        parent_id = graphene.ID(description='Идентификатор родительской строки')
        index = graphene.Int(required=True, description='Индекс вставки')
        global_index = graphene.Int(required=True, description='Индекс вставки в плоскую структуру')
        global_indices = graphene.List(
            graphene.NonNull(GlobalIndicesInputType),
            required=True,
            description='Вспомогательные индексы в плоской структуре'
        )

    row_dimension = graphene.Field(RowDimensionType, required=True, description='Добавленная строка')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        document_id: Optional[str],
        sheet_id: int,
        parent_id: Optional[str],
        index: int,
        global_index: int,
        global_indices: list[GlobalIndicesInputType]
    ):
        return AddRowDimensionMutation(
            row_dimension=add_row_dimension(
                user=info.context.user,
                sheet=get_object_or_404(Sheet, pk=sheet_id),
                document=get_object_or_404(Document, pk=from_global_id(document_id)[1]),
                parent_id=int(parent_id) if parent_id else None,
                index=index,
                global_index=global_index,
                global_indices_map={int(i.row_id): i.global_index for i in global_indices}
            )
        )


class ChangeRowDimensionMutation(BaseMutation):
    """Изменение строки."""

    class Input:
        row_dimension_id = graphene.ID(required=True, description='Идентификатор строки')
        height = graphene.Int(description='Высота строки')
        fixed = graphene.Boolean(required=True, description='Фиксация строки')
        hidden = graphene.Boolean(required=True, description='Скрытие строки')
        dynamic = graphene.Boolean(required=True, description='Динамическая ли строка')

    row_dimension_id = graphene.ID(required=True, description='Идентификатор строки')
    height = graphene.Int(description='Высота строки')
    fixed = graphene.Boolean(required=True, description='Фиксация строки')
    hidden = graphene.Boolean(required=True, description='Скрытие строки')
    dynamic = graphene.Boolean(required=True, description='Динамическая ли строка')
    updated_at = graphene.DateTime(required=True, description='Дата обновления строки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        row_dimension_id: str,
        height: Optional[int],
        fixed: bool,
        hidden: bool,
        dynamic: bool
    ):
        row_dimension = change_row_dimension(
            get_object_or_404(RowDimension, pk=row_dimension_id),
            height=height,
            fixed=fixed,
            hidden=hidden,
            dynamic=dynamic
        )
        return ChangeRowDimensionMutation(
            row_dimension_id=row_dimension.pk,
            height=row_dimension.height,
            fixed=row_dimension.fixed,
            hidden=row_dimension.hidden,
            dynamic=row_dimension.dynamic,
            updated_at=row_dimension.updated_at
        )


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

        - strong - true, false
        - italic - true, false
        - strike - true, false
        - underline - [None, 'single', 'double', 'single_accounting', 'double_accounting']
        - horizontal_align - ['left', 'center', 'right']
        - vertical_align - ['top', 'middle', 'bottom']
        - size - число от 6 до 24
        - kind - [
            'n', 's', 'f', 'b', 'inlineStr', 'e', 'str', 'd', 'text', 'money',
            'bigMoney', 'fl', 'user', 'department', 'organization', 'classification'
        ]
    """

    class Input:
        cell_ids = graphene.List(graphene.NonNull(graphene.ID), required=True, description='Идентификаторы ячеек')
        field = graphene.String(required=True, description='Идентификатор поля')
        value = graphene.String(description='Значение поля')

    changed_options = graphene.List(
        graphene.NonNull(ChangedCellOption),
        description='Измененные свойства ячеек'
    )

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        cell_ids: list[int],
        field: str,
        value: Optional[str] = None
    ):
        field = snakecase(field)
        match CheckCellOptions(field, value):
            case CheckCellOptions.Error(field, error):
                return ChangeCellsOptionMutation(success=False, errors=[ErrorFieldType(field, [error])])
            case CheckCellOptions.Success(value):
                cells = Cell.objects.filter(pk__in=cell_ids).all()
                return ChangeCellsOptionMutation(changed_options=change_cells_option(cells, field, value))


class ChangeValueMutation(BaseMutation):
    """Изменение значения ячейки."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')
        column_id = graphene.ID(required=True, description='Идентификатор колонки')
        row_id = graphene.ID(required=True, description='Идентификатор строки')
        value = graphene.String(required=True, description='Значение')

    value = graphene.String(required=True, description='Измененное значение')
    updated_at = graphene.DateTime(required=True, description='Дата изменения')

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
        result = update_or_create_value(
            document=document,
            sheet=sheet,
            column_id=column_id,
            row_id=row_id,
            value=value
        )
        return ChangeValueMutation(value=result.value.value, updated_at=result.updated_at)


class ChangeFileValueMutation(BaseMutation):
    """Изменение значения ячейки типа `Файл`."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')
        column_id = graphene.ID(required=True, description='Идентификатор колонки')
        row_id = graphene.ID(required=True, description='Идентификатор строки')
        value = graphene.String(required=True, description='Значение')
        remaining_files = graphene.List(graphene.NonNull(graphene.ID), required=True, description='Оставшиеся файлы')
        new_files = graphene.List(graphene.NonNull(Upload), required=True, description='Новые файлы')

    value = graphene.String(required=True, description='Измененное значение')
    updated_at = graphene.DateTime(required=True, description='Дата изменения')
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
        result = update_or_create_file_value(
            user=info.context.user,
            document=document,
            sheet=sheet,
            column_id=column_id,
            row_id=row_id,
            value=value,
            remaining_files=[int(from_global_id(global_id)[1]) for global_id in remaining_files],
            new_files=new_files
        )
        return ChangeFileValueMutation(
            value=result.value.value,
            updated_at=result.updated_at,
            value_files=get_file_value_files(result.value)
        )


class UnloadFileValueArchiveMutation(BaseMutation):
    """Выгрузка архива значения ячейки типа `Файл`."""

    class Input:
        value_id = graphene.ID(required=True, description='Идентификатор значения ячейки')

    src = graphene.String(description='Ссылка на сгенерированный архив')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, value_id: str):
        return UnloadFileValueArchiveMutation(src=create_file_value_archive(get_object_or_404(Value, pk=value_id)))


class SheetMutations(graphene.ObjectType):
    """Список мутаций для работы с листами документа."""

    change_column_dimension = ChangeColumnDimensionMutation.Field(required=True, description='Изменение колонки')

    add_row_dimension = AddRowDimensionMutation.Field(required=True, description='Добавление строки')
    change_row_dimension = ChangeRowDimensionMutation.Field(required=True, description='Изменение строки')
    delete_row_dimension = DeleteRowDimensionMutation.Field(required=True, description='Удаление строки')

    change_cells_option = ChangeCellsOptionMutation.Field(required=True, description='Изменения опций ячейки')

    change_value = ChangeValueMutation.Field(required=True, description='Изменение значения ячейки')
    change_file_value = ChangeFileValueMutation.Field(
        required=True,
        description='Изменение значения ячейки типа `Файл`'
    )
    unload_file_value_archive = UnloadFileValueArchiveMutation.Field(
        required=True,
        description='Выгрузка архива значения ячейки типа `Файл`'
    )
