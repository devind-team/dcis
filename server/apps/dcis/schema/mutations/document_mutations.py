from collections import OrderedDict
from io import BytesIO
from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from devind_helpers.schema.types import TableCellType, TableRowType, TableType
from devind_helpers.utils import gid2int
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import Document, DocumentScan, DocumentStatus, Period, RowDimension, Sheet, Status
from apps.dcis.schema.mutations.sheet_mutations import DeleteRowDimensionMutation
from apps.dcis.schema.types import (
    DocumentMessageType,
    DocumentScanType,
    DocumentStatusType,
    DocumentType,
    GlobalIndicesInputType,
    RowDimensionType,
)
from apps.dcis.services.add_document_data_services import add_document_data
from apps.dcis.services.document_services import (
    create_document,
    create_document_message,
    delete_document_scan,
    upload_document_scan,
)
from apps.dcis.services.document_unload_services import unload_document
from apps.dcis.services.row_dimension_services import (
    add_child_row_dimension,
    change_row_dimension_height,
    delete_child_row_dimension,
)
from apps.dcis.services.status_services import add_document_status, delete_document_status


class AddDocumentMutation(BaseMutation):
    """Добавление документа."""

    class Input:
        """Входные параметры мутации.

          - period_id - идентификатор периода
          - status_id - идентификатор устанавливаемого статуса
          - division_id - идентификатор дивизиона
          - document_id - идентификатор документа, от которого создавать копию
        """
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
        period_id: str,
        status_id: str,
        document_id: str | None = None,
        division_id: str | None = None,
    ) -> 'AddDocumentMutation':
        """Мутация для добавления документа."""
        period = get_object_or_404(Period, pk=gid2int(period_id))
        status = get_object_or_404(Status, pk=status_id)
        document_id: int | None = from_global_id(document_id)[1] if document_id else None
        document, errors = create_document(
            user=info.context.user,
            period=period,
            status=status,
            document_id=document_id,
            division_id=gid2int(division_id)
        )
        return AddDocumentMutation(success=not errors, errors=errors, document=document)


class AddDocumentMessageMutation(BaseMutation):
    """Добавление комментария к документу"""

    class Input:
        document_id = graphene.ID(required=True, description='Документ')
        message = graphene.String(description='Текст комментария')
        kind = graphene.String(description='Тип сообщения')

    document_message = graphene.Field(DocumentMessageType, description='Созданный комментарий')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_id: str, message: str, kind: str):
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        return AddDocumentMessageMutation(
            document_message=create_document_message(info.context.user, document, message, kind)
        )


class AddDocumentStatusMutation(BaseMutation):
    """Добавление статуса документа."""

    class Input:
        document_id = graphene.ID(required=True, description='Документ')
        status_id = graphene.ID(required=True, description='Статус')
        comment = graphene.String(description='Комментарий')

    document_status = graphene.Field(DocumentStatusType, description='Статус документа')
    table = graphene.Field(TableType, description='Документ с ошибками')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_id: str, status_id: str, comment: str):
        document: Document = get_object_or_404(Document, pk=from_global_id(document_id)[1])
        status: Status = get_object_or_404(Status, pk=status_id)
        try:
            return AddDocumentStatusMutation(
                document_status=add_document_status(
                    user=info.context.user,
                    document=document,
                    status=status,
                    comment=comment,
                )
            )
        except ValidationError as error:
            headers_map = OrderedDict()
            headers_map['form'] = 'Форма'
            headers_map['formula'] = 'Формула'
            headers_map['error_message'] = 'Ошибка'
            headers_map['dependencies'] = 'Зависимости'
            rows: list[TableRowType] = []
            for i, le in enumerate(error.params):
                rows.append(
                    TableRowType(
                        index=i,
                        cells=[TableCellType(header=v, value=getattr(le, k)) for k, v in headers_map.items()]
                    )
                )
            return AddDocumentStatusMutation(
                success=False,
                table=TableType(
                    headers=headers_map.values(),
                    rows=rows
                )
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


class AddDocumentDataMutation(BaseMutation):
    """Загрузка данных из файла."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        file = Upload(required=True, description='Файл с данными')
        status_id = graphene.ID(required=True, description='Статус')

    documents = graphene.List(DocumentType, description='Список созданных документов')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        period_id: str,
        file: InMemoryUploadedFile,
        status_id: str
    ) -> 'AddDocumentDataMutation':
        documents, errors = add_document_data(
            info.context.user,
            period_id,
            BytesIO(file.read()),
            status_id
        )
        return AddDocumentDataMutation(
            success=not errors,
            errors=errors,
            documents=documents
        )


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
        return UnloadDocumentMutation(
            src=unload_document(
                user=info.context.user,
                document_id=gid2int(document_id),
                additional=additional
            )
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
        row_dimension = change_row_dimension_height(info.context.user, row_dimension, height)
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
        return DeleteRowDimensionMutation(row_dimension_id=delete_child_row_dimension(info.context.user, row_dimension))


class UploadDocumentScanMutation(BaseMutation):
    """Мутация для загрузки скана документа."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        scan_file = Upload(required=True, description='Загружаемый файл скана')

    document_scan = graphene.Field(DocumentScanType, required=True, description='Скан документа')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root, info: ResolveInfo, document_id: str, scan_file: InMemoryUploadedFile):
        document: Document = get_object_or_404(Document, pk=gid2int(document_id))
        return UploadDocumentScanMutation(
            document_scan=upload_document_scan(info.context.user, document, scan_file)
        )


class DeleteDocumentScanMutation(BaseMutation):
    """Мутация для полного удаления скана документа."""

    class Input:
        file_id = graphene.ID(required=True, description='Идентификатор файла')

    id = graphene.ID(required=True, description='Идентификатор удаляемого файла')

    @staticmethod
    @permission_classes([IsAuthenticated])
    def mutate_and_get_payload(root, info: ResolveInfo, file_id: str, *args, **kwargs):
        file: DocumentScan = get_object_or_404(DocumentScan, pk=file_id)
        delete_document_scan(info.context.user, file)
        return DeleteDocumentScanMutation(id=file_id)


class DocumentMutations(graphene.ObjectType):
    """Мутации, связанные с документами."""

    add_document = AddDocumentMutation.Field(required=True)
    add_document_message = AddDocumentMessageMutation.Field(required=True)
    add_document_status = AddDocumentStatusMutation.Field(required=True)
    delete_document_status = DeleteDocumentStatusMutation.Field(required=True)
    unload_document = UnloadDocumentMutation.Field(required=True)
    add_document_data = AddDocumentDataMutation.Field(required=True)
    upload_document_scan = UploadDocumentScanMutation.Field(required=True)
    delete_document_scan = DeleteDocumentScanMutation.Field(required=True)

    add_child_row_dimension = AddChildRowDimensionMutation.Field(required=True)
    change_child_row_dimension_height = ChangeChildRowDimensionHeightMutation.Field(required=True)
    delete_child_row_dimension = DeleteChildRowDimensionMutation.Field(required=True)
