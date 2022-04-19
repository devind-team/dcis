from typing import Any, Optional, List

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.schema.types import ErrorFieldType
from django.db import transaction
from django.db.models import F
from graphene_django_cud.mutations import DjangoUpdateMutation
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.helpers import DjangoCudBaseMutation
from apps.dcis.models import Document, RowDimension, Sheet, ColumnDimension, Cell
from apps.dcis.schema.types import ColumnDimensionType, RowDimensionType, CellType, MergedCellType
from apps.dcis.services.cell import check_cell_options


class AddRowDimensionMutation(BaseMutation):
    """Вставка строк.

    После добавления строки бы то не было, строка приобретает новый индекс,
    соответственно, все строки после вставленной строки должны увеличить свой индекс на единицу.
    """

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        row_id = graphene.Int(required=True, description='Идентификатор строки')
        position = graphene.String(required=True, description='Позиция вставки')

    row_dimension = graphene.Field(RowDimensionType, required=True, description='Добавленная строка')
    cells = graphene.List(CellType, required=True, description='Добавленные ячейки')
    merged_cells = graphene.List(MergedCellType, required=True, description='Объединенные ячейки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, document_id: str, row_id: int, position: str):
        if position not in ['before', 'after']:
            return AddRowDimensionMutation(
                success=False,
                errors=[ErrorFieldType('position', ['Параметр позиции {position} не из списка: before, after'])]
            )
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        row: RowDimension = get_object_or_404(RowDimension, pk=row_id)
        insert_index = row.index if position == 'before' else row.index + 1
        sheet: Sheet = Sheet.objects.get(pk=row.sheet_id)
        sheet.rowdimension_set.filter(index__gte=insert_index).update(index=F('index') + 1)
        row_dimension = RowDimension.objects.create(
            sheet=sheet,
            index=insert_index,
            document=document,
            user=info.context.user
        )
        cells = [Cell.objects.create(row=row_dimension, column=column) for column in sheet.columndimension_set.all()]
        sheet.move_merged_cells(insert_index, 1)
        return AddRowDimensionMutation(
            row_dimension=row_dimension,
            cells=cells,
            merged_cells=sheet.mergedcell_set.all()
        )


class DeleteRowDimensionMutation(BaseMutation):
    """Мутация для удаления строки."""

    class Input:
        row_id = graphene.Int(required=True, description='Идентификатор строки')

    row_id = graphene.Int(required=True, description='Идентификатор удаленной строки')
    index = graphene.Int(required=True, description='Измененные строки')
    merged_cells = graphene.List(MergedCellType, required=True, description='Объединенные ячейки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, row_id: int):
        row: RowDimension = get_object_or_404(RowDimension, pk=row_id)
        sheet: Sheet = Sheet.objects.get(pk=row.sheet_id)
        row.delete()
        sheet.rowdimension_set.filter(index__gt=row.index).update(index=F('index') - 1)
        sheet.move_merged_cells(row.index, -1, True)
        return DeleteRowDimensionMutation(row_id=row_id, index=row.index, merged_cells=sheet.mergedcell_set.all())


class ChangeColumnDimensionPayload(DjangoCudBaseMutation, DjangoUpdateMutation):
    """Мутация для изменения стилей колонки таблицы."""

    class Meta:
        model = ColumnDimension
        only_fields = ('width', 'fixed', 'hidden', 'auto_size',)
        required_fields = ('fixed', 'hidden', 'auto_size')
        login_required = True
        permissions = ('dcis.change_columndimension',)

    column_dimension = graphene.Field(ColumnDimensionType, description='Измененные стили колонки таблицы')


class ChangeCellsOptionMutation(BaseMutation):
    """Мутация для изменения свойств ячеек:

        - horizontal_align - ['left', 'center', 'right']
        - vertical_align - ['top', 'middle', 'bottom']
        - size - цифра от 10 до 24
        - strong - true, false
        - italic - true, false
        - underline - [None, 'single', 'double', 'single_accounting', 'double_accounting']
        - kind - ['n', 's', 'f', 'b', 'inlineStr', 'e', 'str', 'd', 'text', 'money', 'bigMoney', 'fl', 'user', 'department', 'organization']
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
            cells_id: List[int],
            field: str,
            value: Optional[str] = None
    ):
        success, value, errors = check_cell_options(field, value)
        if not success:
            return ChangeCellsOptionMutation(success=success, errors=errors)
        cells: List[Cell] = Cell.objects.filter(pk__in=cells_id).all()
        with transaction.atomic():
            for cell in cells:
                setattr(cell, field, value)
                cell.save(update_fields=(field,))
        return ChangeCellsOptionMutation(cells=cells)


class SheetMutations(graphene.ObjectType):
    """Список мутаций для работы с листами документа."""

    add_row_dimension = AddRowDimensionMutation.Field(required=True, description='Добавление строки')
    delete_row_dimension = DeleteRowDimensionMutation.Field(required=True, description='Удаление строки')

    change_column_dimension = ChangeColumnDimensionPayload.Field(
        required=True,
        description='Изменение стилей колонки таблицы'
    )

    change_cells_option = ChangeCellsOptionMutation.Field(required=True, description='Изменения опций ячейки')
