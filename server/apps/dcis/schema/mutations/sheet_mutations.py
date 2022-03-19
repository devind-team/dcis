from typing import Any

import graphene
from graphql import ResolveInfo
from django.db.models import F
from graphql_relay import from_global_id
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.decorators import permission_classes
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.schema.types import ErrorFieldType
from django.db import transaction

from apps.dcis.models import Document, RowDimension, Sheet, Cell
from apps.dcis.schema.types import RowDimensionType, CellType, MergedCellType


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
        # Нужно будет добавить ограничение по документу
        sheet.rowdimension_set.filter(index__gte=insert_index).update(index=F('index') + 1)
        # Обновляем объединенные ячейки

        # 1 1 <- insert_index
        # 2 2
        # 3 3
        # 4 4 max_row
        # 5 5 <- insert_index

        # 1. min_row > insert_index && max_row > insert_index -> min_row + 1, max_row + 1
        # 2. min_row <= insert_index && max_row > insert_index -> max_row + 1

        with transaction.atomic():
            print(insert_index)
            sheet.mergedcell_set\
                .filter(min_row__gt=insert_index, max_row__gt=insert_index)\
                .update(min_row=F('min_row') + 1, max_row=F('max_row') + 1)
            sheet.mergedcell_set\
                .filter(min_row__lte=insert_index, max_row__gt=insert_index + 1)\
                .update(max_row=F('max_row') + 1)
        row_dimension = RowDimension.objects.create(sheet=sheet, index=insert_index, document=document)
        cells = [Cell.objects.create(row=row_dimension, column=column) for column in sheet.columndimension_set.all()]
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
        # 1. Удаляем merged_cells если у нас объединения на той же строке, которую удаляем
        sheet.mergedcell_set.filter(min_row=row.index, max_row=row.index).all().delete()
        # 2. Уменьшаем индексы строки на один
        sheet.rowdimension_set.filter(index__gt=row.index).update(index=F('index') - 1)
        # 3. Уменьшаем значения индексов на один
        sheet.mergedcell_set\
            .filter(min_row__gt=row.index)\
            .update(min_row=F('min_row') - 1, max_row=F('max_row') - 1)
        # 4. Удаляем объединения в одну ячейку
        sheet.mergedcell_set.filter(min_col=F('max_col'), min_row=F('max_row')).all().delete()
        return DeleteRowDimensionMutation(row_id=row_id, index=row.index, merged_cells=sheet.mergedcell_set.all())


class SheetMutations(graphene.ObjectType):
    """Список мутаций для работы с листами документа."""

    add_row_dimension = AddRowDimensionMutation.Field(required=True)
    delete_row_dimension = DeleteRowDimensionMutation.Field(required=True)
