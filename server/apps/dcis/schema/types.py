import graphene
from devind_core.schema.types import FileType, ContentTypeType
from devind_helpers.optimized import OptimizedDjangoObjectType
from devind_helpers.schema.connections import CountableConnection
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django_optimizer import resolver_hints
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
from ..filters import ProjectFilter


class ProjectType(OptimizedDjangoObjectType):
    """Тип модели проектов."""

    periods = graphene.List(lambda: PeriodType, description='Периоды')
    user = graphene.Field(UserType, required=True, description='Пользователь')

    class Meta:
        model = Project
        interfaces = (graphene.relay.Node,)
        fields = ('id', 'name', 'short', 'description', 'visibility', 'created_at', 'updated_at', 'user',)
        filterset_class = ProjectFilter
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
    documents = graphene.List(lambda: DocumentType, description='Собираемые документв')

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
            'project',
            'methodical_support',
            'documents',
        )

    @staticmethod
    @resolver_hints(model_field='')
    def resolve_documents(period: Period, info: ResolveInfo, *args, **kwargs):
        return period.document_set.all()


class DivisionType(OptimizedDjangoObjectType):
    """Список участвующих дивизионов в сборе."""

    period = graphene.Field(PeriodType, required=True, description='Период')
    content_type = graphene.Field(ContentTypeType, required=True, description='Дивизион: Department, Organizations')

    class Meta:
        model = Division
        interfaces = (graphene.relay.Node,)
        fields = ('id', 'period', 'content_type', 'object_id',)
        connection_class = CountableConnection


class PrivilegeType(DjangoObjectType):
    """Список сквозных привилегий."""

    class Meta:
        model = Privilege
        fields = '__all__'


class PeriodGroupType(DjangoObjectType):
    """Группы с содержанием привилегий."""

    period = graphene.Field(PeriodType, required=True, description='Период сбора')
    users = DjangoListField(UserType)
    privileges = DjangoListField(PrivilegeType)

    class Meta:
        model = PeriodGroup
        fields = ('id', 'name', 'created_at', 'period', 'users', 'privileges',)


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
    """Тип моделей листов."""

    period = graphene.Field(PeriodType, description='Период')
    columns = graphene.List(lambda: ColumnDimensionType, description='Колонки')
    rows = graphene.List(lambda: RowDimensionType, description='Строки')
    cells = graphene.List(lambda: CellType, description='Мета информация о ячейках')
    merged_cells = graphene.List(lambda: MergedCellType, description='Объединенные ячейки')
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
    def resolve_rows(sheet: Sheet, info: ResolveInfo, *args, **kwargs):
        """Получения всех строк."""
        return sheet.rowdimension_set.all()

    @staticmethod
    def resolve_cells(sheet: Sheet, info: ResolveInfo, *args, **kwargs):
        """Получаем все ячейки, связанные с колонками.

        Можно доставать и по строкам и по столбцам, однако разницы нет, так как таблица квадратная.
        """
        return Cell.objects.filter(column_id__in=sheet.columndimension_set.values_list('pk', flat=True)).all()

    @staticmethod
    def resolve_merged_cells(sheet: Sheet, info: ResolveInfo, *args, **kwargs):
        """Получение всех объединенных ячеек связанных с листом."""
        return MergedCell.objects.filter(sheet=sheet).all()

    @staticmethod
    def resolve_values(sheet: Sheet, info: ResolveInfo, document_id: str, *args, **kwargs):
        """Получение значений, связанных с листом."""
        return Value.objects.filter(sheet=sheet, document_id=from_global_id(document_id)[1]).all()


class DocumentType(DjangoObjectType):
    """Тип моделей документа."""

    period = graphene.Field(PeriodType, description='Период сбора')
    sheets = DjangoListField(SheetType, description='Листы')

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
            'content_type',
            'object_id',
        )
        connection_class = CountableConnection


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
    content_type = graphene.Field(ContentTypeType, description='Дивизион')

    class Meta:
        model = ColumnDimension
        fields = (
            'id',
            'index',
            'width',
            'fixed',
            'sheet',
            'user',
            'content_type',
            'object_id'
        )


class RowDimensionType(DjangoObjectType):
    """Тип строк."""

    parent = graphene.Field(lambda: RowDimensionType, description='Родительские строки')
    children = graphene.List(lambda: RowDimensionType, description='Дочерние строки')
    user = graphene.List(UserType, description='Пользователь')
    content_type = graphene.Field(ContentTypeType, description='Дивизион')

    class Meta:
        model = RowDimension
        fields = (
            'id',
            'index',
            'height',
            'sheet',
            'dynamic',
            'aggregation',
            'parent',
            'document',
            'children',
            'user',
            'content_type',
            'object_id'
        )

    @staticmethod
    @resolver_hints(model_field='rowdimension_set')
    def resolve_children(row: RowDimension, info: ResolveInfo, *args, **kwargs):
        return row.rowdimension_set.all()


class CellType(DjangoObjectType):
    """Тип ячейки."""

    column = graphene.Field(ColumnDimensionType, description='Колонка')
    row = graphene.Field(RowDimensionType, description='Строка')
    limitations = graphene.List(lambda: LimitationType, description='Ограничения на ячейку')

    class Meta:
        model = Cell
        fields = (
            'id',
            'kind',
            'formula',
            'comment',
            'default',
            'mask',
            'tooltip',
            'column',
            'row',
            'limitations',
        )

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

    class Meta:
        model = Value
        fields = (
            'id',
            'value',
            'verified',
            'error',
            'document',
            'sheet',
            'column',
            'row',
        )
