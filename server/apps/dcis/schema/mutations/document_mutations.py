
from typing import Optional

import graphene
from devind_dictionaries.models import Department
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from django.contrib.contenttypes.models import ContentType
from django.db.models import Max
from django.http.request import HttpRequest
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.dcis.models import Period, Document, Value, Sheet
from apps.dcis.schema.types import DocumentType, ValueType
from apps.dcis.services.excel_unload import DocumentUnload


class AddDocument(BaseMutation):
    """Добавление документа."""

    class Input:
        comment = graphene.String(required=True, description='Комментарий')
        period_id = graphene.ID(required=True, description='Идентификатор периода')

    document = graphene.Field(DocumentType, description='Созданный документ')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, comment: str, period_id: str):
        period: Period = get_object_or_404(Period, pk=from_global_id(period_id)[1])
        content_type: ContentType = ContentType.objects.get_for_model(Department)    # Временно департаменты
        object_id: int = 1  # Служба поддержки
        max_version: Optional[int] = Document.objects.aggregate(version=Max('version'))['version']
        document = Document.objects.create(
            version=max_version + 1 if max_version is not None else 1,
            comment=comment,
            content_type=content_type,
            object_id=object_id,
            period=period
        )
        document.sheets.add(*period.sheet_set.all())
        return AddDocument(document=document)


class UnloadDocumentMutation(BaseMutation):
    """Выгрузка документа."""

    class Input:
        document_id = graphene.ID(required=True, description='Документ')

    src = graphene.String(description='Ссылка на сгенерированный файл')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, document_id: str):
        document = Document.objects.get(pk=from_global_id(document_id)[1])
        du: DocumentUnload = DocumentUnload(document, HttpRequest.get_host(info.context))
        src: str = du.xlsx()
        return UnloadDocumentMutation(src=src)


class ChangeValue(BaseMutation):
    """Изменение значения."""

    class Input:
        document_id = graphene.ID(required=True, description='Идентификатор документа')
        sheet_id = graphene.Int(required=True, description='Иднтификатор листа')
        column_id = graphene.Int(required=True, description='Идентификатор колонки')
        row_id = graphene.Int(required=True, description='Идентификатор строки')
        value = graphene.String(required=True, description='Значение')

    value = graphene.Field(ValueType, description='Измененное значение')

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
        # cell: Cell = Cell.objects.get(column_id=column_id, row_id=row_id)
        # В зависимости от типа применяем форматирование
        val, created = Value.objects.update_or_create(
            column_id=column_id,
            row_id=row_id,
            document=document,
            sheet=sheet,
            defaults={
                'value': value
            }
        )
        return ChangeValue(value=val)


class DocumentMutations(graphene.ObjectType):
    """Мутации, связанные с документами."""

    add_document = AddDocument.Field(required=True)
    unload_document = UnloadDocumentMutation.Field(required=True)

    change_value = ChangeValue.Field(required=True)
