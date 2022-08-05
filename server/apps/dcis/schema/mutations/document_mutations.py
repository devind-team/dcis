from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import Document, DocumentStatus, Period, RowDimension, Sheet, Status
from apps.dcis.schema.mutations.sheet_mutations import DeleteRowDimensionMutation
from apps.dcis.schema.types import DocumentStatusType, DocumentType, GlobalIndicesInputType, RowDimensionType
from apps.dcis.services.document_services import (
    add_document_status,
    change_document_comment,
    create_document,
    delete_document_status
)
from apps.dcis.services.document_unload_services import document_upload
from apps.dcis.services.sheet_services import (
    add_child_row_dimension,
    change_row_dimension_height,
    delete_row_dimension,
)


class AddDocumentMutation(BaseMutation):
    """Добавление документа."""

    class Input:
        """Входные параметры мутации.

          - comment - комментарий к документу
          - period_id - идентификатор периода
          - status_id - идентификатор устанавливаемого статуса
          - division_id - идентификатор дивизиона
          - document_id - идентификатор документа, от которого создавать копию
        """
        comment = graphene.String(required=True, description='Комментарий')
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        status_id = graphene.ID(required=True, description='Идентификатор начального статуса документа')
        division_id = graphene.ID(description='Идентификатор дивизиона')
        document_id = graphene.ID(description='Идентификатор документа, от которого создавать копию')

    document = graphene.Field(DocumentType, description='Созданный документ')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: None,
        info: ResolveInfo,
        comment: str,
        period_id: str,
        status_id: str,
        document_id: str | None = None,
        division_id: str | None = None,
    ) -> 'AddDocumentMutation':
        """Мутация для добавления документа."""
        period = get_object_or_404(Period, pk=period_id)
        document_id: int | None = from_global_id(document_id)[1] if document_id else None
        document = create_document(
            user=info.context.user,
            period=period,
            status_id=status_id,
            comment=comment,
            document_id=document_id,
            division_id=division_id
        )
        return AddDocumentMutation(document=document)


class ChangeDocumentCommentMutation(BaseMutation):
    """Изменение комментария версии документа."""

    class Input:
        comment = graphene.String(required=True, description='Комментарий')
        document_id = graphene.ID(description='Идентификатор документа')

    document = graphene.Field(DocumentType, description='Созданный документ')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: None,
        info: ResolveInfo,
        document_id: str,
        comment: str,
    ):
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        return ChangeDocumentCommentMutation(document=change_document_comment(info.context.user, document, comment))


class AddDocumentStatusMutation(BaseMutation):
    """Добавление статуса документа."""

    class Input:
        document_id = graphene.ID(required=True, description='Документ')
        status_id = graphene.ID(required=True, description='Статус')
        comment = graphene.String(description='Комментарий')

    document_status = graphene.Field(DocumentStatusType, description='Статус документа')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_id: str, status_id: str, comment: str):
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        status: Status = get_object_or_404(Status, pk=status_id)
        return AddDocumentStatusMutation(document_status=add_document_status(
            status,
            document,
            comment,
            info.context.user)
        )


class DeleteDocumentStatusMutation(BaseMutation):
    """Удаление статуса документа."""

    class Input:
        document_status_id = graphene.ID(required=True, description='Идентификатор статуса документа')

    id = graphene.ID(required=True, description='Идентификатор статуса документа')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_status_id: int):
        status = get_object_or_404(DocumentStatus, pk=document_status_id)
        delete_document_status(info.context.user, status)
        return DeleteDocumentStatusMutation(id=document_status_id)


class UnloadDocumentMutation(BaseMutation):
    """Выгрузка документа."""

    class Input:
        document_id = graphene.ID(required=True, description='Документ')
        additional = graphene.List(
            graphene.NonNull(graphene.String, required=True),
            description='Дополнительные параметры'
        )

    src = graphene.String(description='Ссылка на сгенерированный файл')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_id: str, additional: list[str] | None = None):
        return UnloadDocumentMutation(src=document_upload(
            user=info.context.user,
            get_host=info.context.get_host(),
            document_id=document_id,
            additional=additional)
        )


class AddChildRowDimensionMutation(BaseMutation):
    """Добавление дочерней строки."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        sheet_id = graphene.ID(required=True, description='Идентификатор листа')
        parent_id = graphene.ID(required=True, description='Идентификатор родительской строки')
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
        root: None,
        info: ResolveInfo,
        document_id: str,
        sheet_id: str,
        parent_id: str,
        index: int,
        global_index: int,
        global_indices: list[GlobalIndicesInputType]
    ):
        document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        parent = get_object_or_404(RowDimension, pk=parent_id)
        sheet = get_object_or_404(Sheet, pk=sheet_id)
        return AddChildRowDimensionMutation(
            row_dimension=add_child_row_dimension(
                user=info.context.user,
                context=info.context,
                sheet=sheet,
                document=document,
                parent=parent,
                index=index,
                global_index=global_index,
                global_indices_map={int(i.row_id): i.global_index for i in global_indices}
            )
        )


class ChangeChildRowDimensionHeightMutation(BaseMutation):
    """Изменение высоты дочерней строки."""

    class Input:
        row_dimension_id = graphene.ID(required=True, description='Идентификатор строки')
        height = graphene.Int(description='Высота строки')

    row_dimension_id = graphene.ID(required=True, description='Идентификатор строки')
    height = graphene.Int(description='Высота строки')
    updated_at = graphene.DateTime(required=True, description='Дата обновления строки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, row_dimension_id: str, height: int):
        row_dimension = get_object_or_404(RowDimension, pk=row_dimension_id)
        row_dimension = change_row_dimension_height(info, row_dimension, height)
        return ChangeChildRowDimensionHeightMutation(
            row_dimension_id=row_dimension.id,
            height=row_dimension.height,
            updated_at=row_dimension.updated_at
        )


class DeleteChildRowDimensionMutation(BaseMutation):
    """Удаление дочерней строки."""

    class Input:
        row_dimension_id = graphene.ID(required=True, description='Идентификатор строки')

    row_dimension_id = graphene.ID(required=True, description='Идентификатор удаленной строки')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, row_dimension_id: str):
        row_dimension = get_object_or_404(RowDimension, pk=row_dimension_id)
        return DeleteRowDimensionMutation(row_dimension_id=delete_row_dimension(info, row_dimension))


class DocumentMutations(graphene.ObjectType):
    """Мутации, связанные с документами."""

    add_document = AddDocumentMutation.Field(required=True)
    change_document_comment = ChangeDocumentCommentMutation.Field(required=True)
    add_document_status = AddDocumentStatusMutation.Field(required=True)
    delete_document_status = DeleteDocumentStatusMutation.Field(required=True)
    unload_document = UnloadDocumentMutation.Field(required=True)

    add_child_row_dimension = AddChildRowDimensionMutation.Field(required=True)
    change_child_row_dimension_height = ChangeChildRowDimensionHeightMutation.Field(required=True)
    delete_child_row_dimension = DeleteChildRowDimensionMutation.Field(required=True)
