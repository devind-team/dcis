"""Мутации, связанные с ограничениями, накладываемыми на лист."""

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

from apps.dcis.models import Limitation, Period
from apps.dcis.schema.types import LimitationType
from apps.dcis.services.limitation_services import (
    add_limitation,
    change_limitation,
    delete_limitation,
    update_limitations_from_file,
)


class UpdateLimitationsFromFileMutation(BaseMutation):
    """Обновление ограничений, накладываемых на лист, из json файла."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        limitations_file = Upload(required=True, description='json файл c ограничениями, накладываемыми на листы')

    limitations = graphene.List(LimitationType, description='Новые ограничения')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: str, limitations_file: InMemoryUploadedFile):
        period = get_object_or_404(Period, pk=gid2int(period_id))
        return UpdateLimitationsFromFileMutation(limitations=update_limitations_from_file(period, limitations_file))


class AddLimitationMutation(BaseMutation):
    """Добавление ограничения, накладываемого на лист."""

    class Input:
        formula = graphene.String(required=True, description='Формула')
        error_message = graphene.String(required=True, description='Сообщение ошибки')
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')

    limitation = graphene.Field(LimitationType, description='Добавленное ограничение')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, formula: str, error_message: str, sheet_id: str):
        return AddLimitationMutation(limitation=add_limitation(formula, error_message, gid2int(sheet_id)))


class ChangeLimitationMutation(BaseMutation):
    """Изменение ограничения, накладываемого на лист."""

    class Input:
        limitation_id = graphene.ID(required=True, description='Идентификатор ограничения')
        formula = graphene.String(required=True, description='Формула')
        error_message = graphene.String(required=True, description='Сообщение ошибки')
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')

    limitation = graphene.Field(LimitationType, description='Измененное ограничение')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        limitation_id: str,
        formula: str,
        error_message: str,
        sheet_id: str
    ):
        limitation = get_object_or_404(Limitation, pk=gid2int(limitation_id))
        return ChangeLimitationMutation(
            limitation=change_limitation(limitation, formula, error_message, gid2int(sheet_id))
        )


class DeleteLimitationMutation(BaseMutation):
    """Удаления ограничения, накладываемого на лист."""

    class Input:
        limitation_id = graphene.ID(required=True, description='Идентификатор ограничения')

    id = graphene.ID(description='Идентификатор удаленного ограничения')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, limitation_id: str):
        limitation = get_object_or_404(Limitation, pk=gid2int(limitation_id))
        return DeleteLimitationMutation(id=delete_limitation(limitation))


class LimitationMutations(graphene.ObjectType):
    """Мутации, связанные с ограничениями, накладываемыми на лист."""

    update_limitations_from_file = UpdateLimitationsFromFileMutation.Field(required=True)
    add_limitation = AddLimitationMutation.Field(required=True)
    change_limitation = ChangeLimitationMutation.Field(required=True)
    delete_limitation = DeleteLimitationMutation.Field(required=True)
