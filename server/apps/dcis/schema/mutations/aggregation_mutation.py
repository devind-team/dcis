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

from apps.dcis.models import Period
from apps.dcis.schema.types import CellAggregationType
from apps.dcis.services.aggregation_services import (
    add_aggregation_cell,
    delete_cells_aggregation,
    unload_aggregations_in_file, update_aggregations_from_file,
)


class UpdateAggregationsFromFileMutation(BaseMutation):
    """Обновление агрегации из json файла."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        aggregations_file = Upload(required=True, description='json файл агрегации ячеек')

    aggregation_cells = graphene.List(CellAggregationType, description='Новая агрегация')

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
            aggregation_cells=update_aggregations_from_file(info.context.user, period, aggregations_file)
        )


class UnloadAggregationsInFileMutation(BaseMutation):
    """Выгрузка агригации периода в json файл."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')

    src = graphene.String(description='Ссылка на сгенерированный файл')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, period_id: str):
        period = get_object_or_404(Period, pk=gid2int(period_id))
        return UnloadAggregationsInFileMutation(
            src=unload_aggregations_in_file(
                user=info.context.user,
                get_host=info.context.get_host(),
                period=period
            )
        )


class AddAggregationMutation(BaseMutation):
    """Добавление агрегации."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        aggregation_cell = graphene.String(required=True, description='Агрегируемая ячейка')
        aggregation_method = graphene.String(required=True, description='Метод агрегации')
        aggregation_cells = graphene.List(graphene.String, description='Агрегируемые ячейки')

    aggregation_cells = graphene.Field(CellAggregationType, description='Добавлена агрегация')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        period_id: str | int,
        aggregation_cell: str,
        aggregation_method: str,
        aggregation_cells: list[str]
    ):
        period = get_object_or_404(Period, pk=gid2int(period_id))
        return AddAggregationMutation(
            aggregation_cells=add_aggregation_cell(
                info.context.user,
                period,
                aggregation_cell,
                aggregation_method,
                aggregation_cells
            )
        )


class DeleteAggregationMutation(BaseMutation):
    """Удаление агрегации."""

    class Input:
        aggregation_cell_id = graphene.ID(required=True, description='Идентификатор агрегирующей ячеуки')

    id = graphene.ID(description='Идентификатор удаленной агрегации')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, aggregation_cell_id: int | str):
        delete_cells_aggregation(info.context.user, aggregation_cell_id)
        return DeleteAggregationMutation(id=aggregation_cell_id)


class AggregationMutations(graphene.ObjectType):
    """Мутации, связанные с агрегацией."""

    update_aggregations_from_file = UpdateAggregationsFromFileMutation.Field(required=True)
    unload_aggregations_in_file = UnloadAggregationsInFileMutation.Field(required=True)
    add_aggregation = AddAggregationMutation.Field(required=True)
    delete_aggregation = DeleteAggregationMutation.Field(required=True)
