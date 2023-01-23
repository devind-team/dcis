from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.schema.types import ErrorFieldType
from graphene.utils.str_converters import to_snake_case
from graphql import ResolveInfo

from apps.dcis.models import ColumnDimension, RowDimension, Sheet
from apps.dcis.permissions.period_permissions import can_change_period
from apps.dcis.schema.types import (
    BaseSheetType,
    CellType,
    ChangeColumnDimensionType,
    ChangeRowDimensionType,
    GlobalIndicesInputType,
    RowDimensionType,
    SheetType,
)
from apps.dcis.services.column_dimension_services import (change_column_dimension, change_column_dimensions_fixed)
from apps.dcis.services.row_dimension_services import (
    add_row_dimension,
    change_row_dimension,
    change_row_dimensions_fixed,
    delete_row_dimension,
)
from apps.dcis.services.sheet_services import rename_sheet


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
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, sheet_id: str, name: str):
        sheet = get_object_or_404(Sheet, pk=sheet_id)
        sheet, cells = rename_sheet(user=info.context.user, sheet=sheet, name=name)
        return RenameSheetMutation(
            sheet=sheet,
            cells=cells
        )


class ChangeShowSheetMutation(BaseMutation):
    """Изменение показа листа."""

    class Input:
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')
        field = graphene.String(required=True, description='Выбор: showHead, showChild')
        value = graphene.Boolean(required=True, description='Значение')

    sheet = graphene.Field(BaseSheetType, description='Измененный лист')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        sheet_id: str,
        field: str,
        value: bool
    ) -> 'ChangeShowSheetMutation':
        if field not in ['showHead', 'showChild']:
            return ChangeShowSheetMutation(
                success=False,
                errors=[ErrorFieldType('field', ['Поле должно быть: showHead, showChild'])]
            )
        field = to_snake_case(field)
        sheet: Sheet = get_object_or_404(Sheet, pk=sheet_id)
        can_change_period(info.context.user, sheet.period)
        setattr(sheet, field, value)
        sheet.save(update_fields=(field,))
        return ChangeShowSheetMutation(sheet=sheet)


class ChangeColumnDimensionMutation(BaseMutation):
    """Изменение колонки."""

    class Input:
        column_dimension_id = graphene.ID(required=True, description='Идентификатор колонки')
        width = graphene.Int(description='Ширина колонки')
        hidden = graphene.Boolean(required=True, description='Скрытие колонки')
        kind = graphene.String(required=True, description='Тип значения')

    column_dimension = graphene.Field(ChangeColumnDimensionType, description='Измененная колонка')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        column_dimension_id: str,
        width: int | None,
        hidden: bool,
        kind: str
    ) -> 'ChangeColumnDimensionMutation':
        column_dimension = get_object_or_404(ColumnDimension, pk=column_dimension_id)
        return ChangeColumnDimensionMutation(
            column_dimension=change_column_dimension(
                user=info.context.user,
                column_dimension=column_dimension,
                width=width,
                hidden=hidden,
                kind=kind
            )
        )


class ChangeColumnDimensionsFixed(BaseMutation):
    """Изменение свойства fixed у колонок."""

    class Input:
        column_dimension_ids = graphene.List(
            graphene.NonNull(graphene.ID),
            required=True,
            description='Идентификаторы колонок'
        )
        fixed = graphene.Boolean(required=True, description='Фиксация колонки')

    column_dimensions = graphene.List(ChangeColumnDimensionType, description='Измененные колонки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        column_dimension_ids: list[str],
        fixed: bool
    ):
        column_dimensions = [get_object_or_404(ColumnDimension, pk=column_id) for column_id in column_dimension_ids]
        return ChangeColumnDimensionsFixed(
            column_dimensions=change_column_dimensions_fixed(
                column_dimensions,
                fixed
            )
        )


class AddRowDimensionMutation(BaseMutation):
    """Добавление строки."""

    class Input:
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')
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
        sheet_id: int,
        index: int,
        global_index: int,
        global_indices: list[GlobalIndicesInputType]
    ):
        sheet = get_object_or_404(Sheet, pk=sheet_id)
        return AddRowDimensionMutation(
            row_dimension=add_row_dimension(
                user=info.context.user,
                sheet=sheet,
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
        hidden = graphene.Boolean(required=True, description='Скрытие строки')
        dynamic = graphene.Boolean(required=True, description='Динамическая ли строка')

    row_dimension = graphene.Field(ChangeRowDimensionType, description='Измененная строка')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        row_dimension_id: str,
        height: int | None,
        hidden: bool,
        dynamic: bool
    ):
        row_dimension = get_object_or_404(RowDimension, pk=row_dimension_id)
        return ChangeRowDimensionMutation(
            row_dimension=change_row_dimension(
                user=info.context.user,
                row_dimension=row_dimension,
                height=height,
                hidden=hidden,
                dynamic=dynamic,
            )
        )


class ChangeRowDimensionsFixed(BaseMutation):
    """Изменение свойства fixed у строк."""

    class Input:
        row_dimension_ids = graphene.List(
            graphene.NonNull(graphene.ID),
            required=True,
            description='Идентификаторы строк'
        )
        fixed = graphene.Boolean(required=True, description='Фиксация строки')

    row_dimensions = graphene.List(ChangeRowDimensionType, description='Измененные строки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        row_dimension_ids: list[str],
        fixed: bool
    ):
        row_dimensions = [get_object_or_404(RowDimension, pk=row_id) for row_id in row_dimension_ids]
        return ChangeRowDimensionsFixed(
            row_dimensions=change_row_dimensions_fixed(
                row_dimensions,
                fixed
            )
        )


class DeleteRowDimensionMutation(BaseMutation):
    """Удаление строки."""

    class Input:
        row_dimension_id = graphene.ID(required=True, description='Идентификатор строки')

    row_dimension_id = graphene.ID(required=True, description='Идентификатор удаленной строки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, row_dimension_id: str):
        row_dimension = get_object_or_404(RowDimension, pk=row_dimension_id)
        return DeleteRowDimensionMutation(
            row_dimension_id=delete_row_dimension(
                user=info.context.user,
                row_dimension=row_dimension,
            )
        )


class SheetMutations(graphene.ObjectType):
    """Список мутаций для работы с листами документа."""

    rename_sheet = RenameSheetMutation.Field(required=True, description='Изменение названия листа')
    change_show_sheet = ChangeShowSheetMutation.Field(required=True, description='Показ листов')

    change_column_dimension = ChangeColumnDimensionMutation.Field(required=True, description='Изменение колонки')
    change_column_dimensions_fixed = ChangeColumnDimensionsFixed.Field(
        required=True,
        description='Изменение свойства fixed у колонок'
    )

    add_row_dimension = AddRowDimensionMutation.Field(required=True, description='Добавление строки')
    change_row_dimension = ChangeRowDimensionMutation.Field(required=True, description='Изменение строки')
    change_row_dimensions_fixed = ChangeRowDimensionsFixed.Field(
        required=True,
        description='Изменение свойства fixed у строк'
    )
    delete_row_dimension = DeleteRowDimensionMutation.Field(required=True, description='Удаление строки')
