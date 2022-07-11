from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.schema.types import ErrorFieldType
from graphql import ResolveInfo
from graphql_relay import from_global_id
from stringcase import snakecase

from apps.dcis.models import Cell, ColumnDimension, RowDimension, Sheet, Value
from apps.dcis.permissions import ChangePeriodSheet
from apps.dcis.schema.types import CellType, ChangedCellOption, GlobalIndicesInputType, RowDimensionType, SheetType

from apps.dcis.models import Cell, ColumnDimension, RowDimension, Sheet
from apps.dcis.schema.types import SheetType, CellType, ChangedCellOption, GlobalIndicesInputType, RowDimensionType
from apps.dcis.permissions import ChangeSheet
from apps.dcis.services.sheet_services import (
    CheckCellOptions,
    add_row_dimension,
    change_cells_option,
    change_column_dimension,
    change_row_dimension,
    delete_row_dimension,
    get_file_value_files,
    rename_sheet,
    update_or_create_file_value,
    update_or_create_value,
)


class RenameSheetMutation(BaseMutation):
    """Изменение названия листа.

    Во время мутации изменяем только формулы и ничего не пересчитываем.
    """

    class Input:
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')
        name = graphene.String(required=True, description='Новое название листа')

    sheet = graphene.Field(SheetType, description='Лист')
    cells = graphene.List(CellType, description='Измененные ячейки')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangePeriodSheet,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, sheet_id: str, name: str):
        sheet, cells = rename_sheet(get_object_or_404(Sheet, pk=sheet_id), name)
        return RenameSheetMutation(
            sheet=sheet,
            cells=cells
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
        width: int | None,
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
        sheet_id = graphene.Int(required=True, description='Идентификатор листа')
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
        document_id: str | None,
        sheet_id: int,
        parent_id: str | None,
        index: int,
        global_index: int,
        global_indices: list[GlobalIndicesInputType]
    ):
        return AddRowDimensionMutation(
            row_dimension=add_row_dimension(
                user=info.context.user,
                sheet=get_object_or_404(Sheet, pk=sheet_id),
                document_id=from_global_id(document_id)[1] if document_id else None,
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
        height: int | None,
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
        row_dimension_id = graphene.ID(required=True, description='Идентификатор строки')

    row_dimension_id = graphene.ID(required=True, description='Идентификатор удаленной строки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, row_dimension_id: str):
        return DeleteRowDimensionMutation(
            row_dimension_id=delete_row_dimension(
                row_dimension=get_object_or_404(RowDimension, pk=row_dimension_id)
            )
        )


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
        value: str | None = None
    ):
        field = snakecase(field)
        match CheckCellOptions(field, value):
            case CheckCellOptions.Error(field, error):
                return ChangeCellsOptionMutation(success=False, errors=[ErrorFieldType(field, [error])])
            case CheckCellOptions.Success(value):
                cells = Cell.objects.filter(pk__in=cell_ids).all()
                return ChangeCellsOptionMutation(changed_options=change_cells_option(cells, field, value))


class SheetMutations(graphene.ObjectType):
    """Список мутаций для работы с листами документа."""

    rename_sheet = RenameSheetMutation.Field(required=True, description='Изменение названия листа')

    change_column_dimension = ChangeColumnDimensionMutation.Field(required=True, description='Изменение колонки')

    add_row_dimension = AddRowDimensionMutation.Field(required=True, description='Добавление строки')
    change_row_dimension = ChangeRowDimensionMutation.Field(required=True, description='Изменение строки')
    delete_row_dimension = DeleteRowDimensionMutation.Field(required=True, description='Удаление строки')

    change_cells_option = ChangeCellsOptionMutation.Field(required=True, description='Изменения опций ячейки')

