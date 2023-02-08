"""Модуль содержит мутации, относящиеся к агрегации."""

from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.utils import gid2int
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo

from apps.dcis.models import Cell, Period
from apps.dcis.schema.types import CellAggregationType
from apps.dcis.services.cell_service import delete_cells_aggregation, update_aggregations_from_file


class UpdateAggregationsFromFileMutation(BaseMutation):
    """Обновление агрегации из json файла."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        aggregations_file = Upload(required=True, description='json файл агрегации ячеек')

    aggregations = graphene.List(CellAggregationType, description='Новая агрегация')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        period_id: str | int,
        aggregations_file: InMemoryUploadedFile
    ):
        period = get_object_or_404(Period, pk=gid2int(period_id))
        return UpdateAggregationsFromFileMutation(
            aggregations=update_aggregations_from_file(info.context.user, period, aggregations_file)
        )


class DeleteAggregationMutation(BaseMutation):
    """Удаление агрегации."""

    class Input:
        aggregation_cell_id = graphene.ID(required=True, description='Идентификатор агрегирующей ячеуки')

    id = graphene.ID(description='Идентификатор удаленной агрегации')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, aggregation_cell_id: int | str):
        return DeleteAggregationMutation(id=delete_cells_aggregation(info.context.user, aggregation_cell_id))


class AggregationMutations(graphene.ObjectType):
    """Мутации, связанные с агрегацией."""

    update_aggregations_from_file = UpdateAggregationsFromFileMutation.Field(required=True)
    delete_aggregation = DeleteAggregationMutation.Field(required=True)
