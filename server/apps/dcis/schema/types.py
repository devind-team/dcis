from typing import Optional

import graphene
from devind_core.schema.types import FileType, ContentTypeType
from devind_dictionaries.models import Department, Organization
from devind_dictionaries.schema import OrganizationType, DepartmentType
from devind_helpers.optimized import OptimizedDjangoObjectType
from devind_helpers.schema.connections import CountableConnection
from django.contrib.contenttypes.models import ContentType
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django_optimizer import resolver_hints
from django.db.models import Q
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.schema import UserType
from ..models import (
    Project, Period, Division,
    Privilege, PeriodGroup, PeriodPrivilege,
    Status, Sheet, Document, DocumentStatus,
    Attribute, AttributeValue, ColumnDimension,
    RowDimension, Cell, Limitation, MergedCell,
    Value
)


class ProjectType(OptimizedDjangoObjectType):
    """Тип модели проектов."""

    periods = graphene.List(lambda: PeriodType, description='Периоды')
    user = graphene.Field(UserType, description='Пользователь')
    content_type = graphene.Field(ContentTypeType, required=True, description='Дивизион: Department, Organizations')

    class Meta:
        model = Project
        interfaces = (graphene.relay.Node,)
        fields = (
            'id',
            'name',
            'short',
            'description',
            'visibility',
            'archive',
            'created_at',
            'updated_at',
            'content_type',
            'user',
        )
        filter_fields = {
            'name': ['icontains'],
            'user': ['exact', 'in']
        }
        connection_class = CountableConnection

    @staticmethod
    @resolver_hints(model_field='period_set')
    def resolve_periods(project: Project, info: ResolveInfo):
        return project.period_set.all()


class PeriodType(DjangoObjectType):
    """Тип периода."""

    user = graphene.Field(UserType, required=True, description='Пользователь')
    project = graphene.Field(ProjectType, description='Проект')
    methodical_support = DjangoListField(FileType)
    # Нужно будет отфильтровать в зависимости от прав пользователя
    documents = graphene.List(lambda: DocumentType, description='Собираемые документов')

    # Нужно вывести все дивизионы специальным образом
    divisions = graphene.List(lambda: DivisionUnionType, description='Участвующие дивизионы')
    period_groups = graphene.List(lambda: PeriodGroupType, description='Группы пользователей назначенных в сборе')

    class Meta:
        model = Period
        fields = (
            'id',
            'name',
            'status',
            'multiple',
            'privately',
            'start',
            'expiration',
            'created_at',
            'updated_at',
            'user',
            'period_groups',
            'project',
            'methodical_support',
            'documents',
        )
        convert_choices_to_enum = False

    @staticmethod
    @resolver_hints(model_field='document_set')
    def resolve_documents(period: Period, info: ResolveInfo, *args, **kwargs):
        return period.document_set.all()

    @staticmethod
    @resolver_hints(model_field='')
    def resolve_divisions(period: Period, info: ResolveInfo, *args, **kwargs):
        divisions = period.division_set.all()
        return Department.objects.filter(pk__in=divisions.values_list('object_id', flat=True)) \
            if ContentType.objects.get_for_id(period.project.content_type_id).model == 'department' \
            else Organization.objects.filter(pk__in=divisions.values_list('object_id', flat=True))

    @staticmethod
    @resolver_hints(model_field='')
    def resolve_period_groups(period: Period, info: ResolveInfo, *args, **kwargs):
        return period.periodgroup_set.all()


class DivisionType(OptimizedDjangoObjectType):
    """Список участвующих дивизионов в сборе."""

    period = graphene.Field(PeriodType, required=True, description='Период')

    class Meta:
        model = Division
        interfaces = (graphene.relay.Node,)
        fields = ('id', 'period', 'object_id',)
        filter_fields = {
            'id': ('exact',),
            'period': ('in', 'exact',),
            'object_id': ('in', 'exact',)
        }
        connection_class = CountableConnection


class DivisionModelType(graphene.ObjectType):
    """Описание обобщенного типа дивизиона."""

    id = graphene.Int(required=True, description='Идентификатор модели дивизиона')
    model = graphene.String(required=True, description='Модель дивизиона: department, organization')
    name = graphene.String(required=True, description='Название дивизиона')


class DivisionUnionType(graphene.Union):
    """Список дивизионов"""

    class Meta:
        types = (OrganizationType, DepartmentType)


class PrivilegeType(DjangoObjectType):
    """Список сквозных привилегий."""

    class Meta:
        model = Privilege
        fields = ('id', 'name', 'created_at', 'key',)


class PeriodGroupType(DjangoObjectType):
    """Группы с содержанием привилегий."""

    period = graphene.Field(PeriodType, required=True, description='Период сбора')
    users = DjangoListField(UserType, description='Пользователи в группе')
    privileges = DjangoListField(PrivilegeType, description='Привилегии группы')

    class Meta:
        model = PeriodGroup
        fields = ('id', 'name', 'created_at', 'period', 'users', 'privileges',)

    @staticmethod
    @resolver_hints(model_field='')
    def resolve_users(period_group: PeriodGroup, info: ResolveInfo, *args, **kwargs):
        return period_group.users.all()


class PeriodPrivilegeType(DjangoObjectType):
    """Тип для отдельных привилегий пользователей."""

    period = graphene.Field(PeriodType, required=True, description='Период')
    user = graphene.Field(UserType, required=True, description='Пользователь')
    privilege = graphene.Field(PrivilegeType, required=True, description='Привилегия')

    class Meta:
        model = PeriodPrivilege
        fields = ('id', 'period', 'user', 'privilege',)


class StatusType(DjangoObjectType):
    """Тип статусов документов."""

    class Meta:
        model = Status
        fields = ('id', 'name', 'edit', 'comment',)


class SheetType(DjangoObjectType):
    """Тип моделей листов.

        rows, cells - могут иметь идентификатор документа, в противном случае
            выгружается только каркас
        values - могут выгружаться только значения привязанные к строкам
        columns, merged_cells - привязываются к каркасу и от документа не зависят.
    """

    period = graphene.Field(PeriodType, description='Период')
    columns = graphene.List(lambda: ColumnDimensionType, description='Колонки')
    merged_cells = graphene.List(lambda: MergedCellType, description='Объединенные ячейки')
    rows = graphene.List(
        lambda: RowDimensionType,
        document_id=graphene.ID(description='Идентификатор документа'),
        description='Строки'
    )
    cells = graphene.List(
        lambda: CellType,
        document_id=graphene.ID(description='Идентификатор документа'),
        description='Мета информация о ячейках'
    )
    values = graphene.List(
        lambda: ValueType,
        document_id=graphene.ID(required=True, description='Идентификатор документа'),
        description='Значения документа'
    )

    class Meta:
        model = Sheet
        fields = (
            'id',
            'name',
            'position',
            'comment',
            'created_at',
            'updated_at',
            'period',
        )

    @staticmethod
    @resolver_hints(model_field='columndimension_set')
    def resolve_columns(sheet: Sheet, info: ResolveInfo, *args, **kwargs):
        """Получение всех колонок."""
        return sheet.columndimension_set.all()

    @staticmethod
    @resolver_hints(model_field='rowdimension_set')
    def resolve_rows(sheet: Sheet, info: ResolveInfo, document_id: Optional[str] = None, *args, **kwargs):
        """Получения всех строк."""
        if document_id is None:
            return sheet.rowdimension_set.filter(parent__isnull=True)
        document_id = from_global_id(document_id)[1]
        return sheet.rowdimension_set.filter(Q(parent__isnull=True) | Q(parent__isnull=False, document_id=document_id))

    @staticmethod
    def resolve_cells(sheet: Sheet, info: ResolveInfo, document_id: Optional[str] = None, *args, **kwargs):
        """Получаем все ячейки, связанные со строками.

            Получение зависит от строк, так как от документа к документу они могут меняться.
        """
        if document_id is None:
            rows_id = sheet.rowdimension_set.filter(parent__isnull=True).values_list('pk', flat=True)
        else:
            document_id = from_global_id(document_id)[1]
            rows_id = sheet.rowdimension_set.filter(
                Q(parent__isnull=True) | Q(parent__isnull=False, document_id=document_id)
            ).values_list('id', flat=True)
        return Cell.objects.filter(row_id__in=rows_id).all()

    @staticmethod
    @resolver_hints(model_field='mergedcell_set')
    def resolve_merged_cells(sheet: Sheet, info: ResolveInfo, *args, **kwargs):
        """Получение всех объединенных ячеек связанных с листом."""
        return sheet.mergedcell_set.all()

    @staticmethod
    @resolver_hints(model_field='value_set')
    def resolve_values(sheet: Sheet, info: ResolveInfo, document_id: str, *args, **kwargs):
        """Получение значений, связанных с листом."""
        return sheet.value_set.filter(document_id=from_global_id(document_id)[1]).all()


class DocumentType(DjangoObjectType):
    """Тип моделей документа."""

    period = graphene.Field(PeriodType, description='Период сбора')
    sheets = DjangoListField(SheetType, description='Листы')
    last_status = graphene.Field(lambda: DocumentStatusType, description='Последний статус документа')

    class Meta:
        model = Document
        interfaces = (graphene.relay.Node,)
        fields = (
            'id',
            'comment',
            'version',
            'created_at',
            'updated_at',
            'period',
            'sheets',
            'object_id',
            'last_status',
        )
        filter_fields = {}
        connection_class = CountableConnection

    @staticmethod
    def resolve_last_status(document: Document, info: ResolveInfo, *args, **kwargs):
        try:
            return document.documentstatus_set.latest('created_at')
        except DocumentStatus.DoesNotExist:
            return None


class DocumentStatusType(DjangoObjectType):
    """Тип статусов для документов."""

    document = graphene.Field(DocumentType, description='Документ')
    status = graphene.Field(StatusType, required=True, description='Установленный статус')
    user = graphene.Field(UserType, required=True, description='Пользователь')

    class Meta:
        model = DocumentStatus
        fields = (
            'id',
            'comment',
            'created_at',
            'document',
            'status',
            'user',
        )


class AttributeType(DjangoObjectType):
    """Тип атрибутов для документов."""

    period = graphene.Field(PeriodType, description='Период')
    parent = graphene.Field(lambda: AttributeType, description='Родительский атрибут')
    children = graphene.List(lambda: AttributeType, description='Дочерние элементы')

    class Meta:
        model = Attribute
        fields = (
            'id',
            'name',
            'placeholder',
            'key',
            'kind',
            'default',
            'mutable',
            'period',
            'parent',
        )

    @staticmethod
    @resolver_hints(model_field='attribute_set')
    def resolve_children(attribute: Attribute, info: ResolveInfo, *args, **kwargs):
        return attribute.attribute_set.all()


class AttributeValueType(DjangoObjectType):
    """Тип со значениями атрибутов."""

    document = graphene.Field(DocumentType, description='Документ')
    attribute = graphene.Field(AttributeType, description='Атрибут')

    class Meta:
        model = AttributeValue
        fields = (
            'id',
            'value',
            'created_at',
            'created_at',
            'document',
            'attribute',
        )


class ColumnDimensionType(DjangoObjectType):
    """Тип колонок."""

    sheet = graphene.Field(SheetType, description='Листы')
    user = graphene.List(UserType, description='Пользователь')
    cells = graphene.List(lambda: CellType, description='Ячейки')
    values = graphene.List(
        lambda: ValueType,
        document_id=graphene.ID(required=True, description='Идентификатор документа'),
        description='Значения документа'
    )

    class Meta:
        model = ColumnDimension
        fields = (
            'id',
            'index',
            'width',
            'fixed',
            'hidden',
            'kind',
            'sheet',
            'user',
            'cells',
            'values',
        )
        convert_choices_to_enum = False

    @staticmethod
    @resolver_hints(model_field='cell_set')
    def resolve_cells(column: ColumnDimension, info: ResolveInfo, *args, **kwargs):
        return column.cell_set.all()

    @staticmethod
    @resolver_hints(model_field='value_set')
    def resolve_values(column: ColumnDimension, info: ResolveInfo, document_id: str, *args, **kwargs):
        """Получение значений, связанных с листом."""
        return column.value_set.filter(document_id=from_global_id(document_id)[1]).all()


class RowDimensionType(DjangoObjectType):
    """Тип строк."""

    parent_id = graphene.Int(description='Идентификатор родителя')
    children = graphene.List(lambda: RowDimensionType, description='Дочерние строки')
    user = graphene.List(UserType, description='Пользователь')
    cells = graphene.List(lambda: CellType, description='Ячейки')

    class Meta:
        model = RowDimension
        fields = (
            'id',
            'index',
            'height',
            'sheet',
            'dynamic',
            'aggregation',
            'object_id',
            'created_at',
            'updated_at',
            'parent',
            'parent_id',
            'document',
            'children',
            'user',
            'cells',
        )
        convert_choices_to_enum = False

    @staticmethod
    @resolver_hints(model_field='rowdimension_set')
    def resolve_children(row: RowDimension, info: ResolveInfo, *args, **kwargs):
        return row.rowdimension_set.all()


class CellType(DjangoObjectType):
    """Тип ячейки."""

    column = graphene.Field(ColumnDimensionType, description='Колонка')
    column_id = graphene.Int(description='Идентификатор колонки')
    row = graphene.Field(RowDimensionType, description='Строка')
    row_id = graphene.Int(description='Идентификатор строки')
    limitations = graphene.List(lambda: LimitationType, description='Ограничения на ячейку')

    class Meta:
        model = Cell
        fields = (
            'id',
            'kind',
            'editable',
            'formula',
            'comment',
            'default',
            'mask',
            'tooltip',
            'column',
            'column_id',
            'row',
            'row_id',
            'horizontal_align',
            'vertical_align',
            'size',
            'strong',
            'italic',
            'strike',
            'underline',
            'color',
            'background',
            'limitations',
            'border_style',
            'border_color'
        )
        convert_choices_to_enum = False

    @staticmethod
    @resolver_hints(model_field='limitation_set')
    def resolve_limitations(cell: Cell, info: ResolveInfo, *args, **kwargs):
        return cell.limitation_set.all()


class LimitationType(DjangoObjectType):
    """Ограничения на ячейку."""

    cell = graphene.Field(CellType, description='Ячейка')

    class Meta:
        model = Limitation
        fields = (
            'id',
            'operator',
            'condition',
            'value',
            'cell',
        )
        convert_choices_to_enum = False


class MergedCellType(DjangoObjectType):
    """Тип для объединенных ячеек."""

    range = graphene.String(required=True, description='Объединенный диапазон')
    colspan = graphene.Int()
    rowspan = graphene.Int()
    target = graphene.String()
    cells = graphene.List(graphene.String)

    class Meta:
        model = MergedCell
        fields = (
            'id',
            'min_col',
            'min_row',
            'max_col',
            'max_row',
            'range',
            'colspan',
            'rowspan',
            'target',
            'cells'
        )

    @staticmethod
    def resolve_range(merge_cell: MergedCell, info: ResolveInfo, *args, **kwargs):
        return str(merge_cell)


class ValueType(DjangoObjectType):
    """Тип для значений."""

    column_id = graphene.Int(description='Идентификатор колонки')
    row_id = graphene.Int(description='Идентификатор строки')

    class Meta:
        model = Value
        fields = (
            'id',
            'value',
            'verified',
            'error',
            'column_id',
            'row_id',
        )
