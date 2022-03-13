from typing import Optional

import graphene
import socket

from django.contrib.contenttypes.models import ContentType
from devind_helpers.schema.mutations import BaseMutation
from devind_dictionaries.models import Department
from graphql import ResolveInfo
from devind_helpers.decorators import permission_classes
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.orm_utils import get_object_or_404
from graphql_relay import from_global_id
from django.db.models import Max

from apps.dcis.models import Period, Document, Value
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
        du: DocumentUnload = DocumentUnload(document_id, socket.gethostname())
        src: str = du.xlsx()
        return UnloadDocumentMutation(src=src)


class ChangeValue(BaseMutation):
    """Изменение значения."""

    class Input:
        value_id = graphene.ID(required=True, description='Идентификатор значения')
        value = graphene.String(required=True, description='Значение')

    value = graphene.Field(ValueType, description='Измененное значение')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: None, info: ResolveInfo, value_id: str, value: str):
        value_obj = Value.objects.get(pk=value_id)
        value_obj.value = value
        value_obj.save()
        return ChangeValue(value=value_obj)


class DocumentMutations(graphene.ObjectType):
    """Мутации, связанные с документами."""

    add_document = AddDocument.Field(required=True)
    unload_document = UnloadDocumentMutation.Field(required=True)

    change_value = ChangeValue.Field(required=True)
