import json

import graphene
from devind_core.schema.types import ContentTypeType, FileType
from devind_dictionaries.models import Organization
from devind_dictionaries.schema import DepartmentType
from devind_helpers.optimized import OptimizedDjangoObjectType
from devind_helpers.schema.connections import CountableConnection
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from graphene_django import DjangoListField, DjangoObjectType
from graphene_django_optimizer import resolver_hints
from graphql import ResolveInfo

from apps.core.models import User
from apps.core.schema import UserType
from apps.dcis.filters import DocumentFilter
from apps.dcis.helpers.exceptions import is_raises
from apps.dcis.models import (
    Attribute, AttributeValue, ColumnDimension, Document,
    DocumentStatus, Limitation, Period,
    PeriodGroup, PeriodPrivilege, Privilege,
    Project, RowDimension, Sheet,
    Status, Value,
)
from apps.dcis.permissions import (
    AddDocumentBase,
    can_add_period_base,
    can_change_document_base,
    can_change_period_divisions_base,
    can_change_period_groups_base,
    can_change_period_settings_base,
    can_change_period_sheet_base,
    can_change_period_users_base,
    can_change_project_base,
    can_delete_period_base,
    can_delete_project_base,
)
from apps.dcis.services.divisions_services import get_period_divisions


class ProjectType(OptimizedDjangoObjectType):
    """Тип модели проектов."""

    periods = graphene.List(lambda: PeriodType, description='Периоды')
    user = graphene.Field(UserType, description='Пользователь')
    content_type = graphene.Field(ContentTypeType, required=True, description='Дивизион: Department, Organizations')

    can_change = graphene.Boolean(required=True, description='Может ли пользователь изменять проект')
    can_delete = graphene.Boolean(required=True, description='Может ли пользователь удалять проект')
    can_add_period = graphene.Boolean(required=True, description='Может ли пользователь добавлять периоды в проект')

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
    def resolve_periods(project: Project, info: ResolveInfo) -> QuerySet[Period]:
        return project.period_set.all()

    @staticmethod
    def resolve_can_change(project: Project, info: ResolveInfo) -> bool:
        return not is_raises(PermissionDenied, can_change_project_base, info.context.user, project)

    @staticmethod
    def resolve_can_delete(project: Project, info: ResolveInfo) -> bool:
        return not is_raises(PermissionDenied, can_delete_project_base, info.context.user, project)

    @staticmethod
    def resolve_can_add_period(project: Project, info: ResolveInfo) -> bool:
        return not is_raises(PermissionDenied, can_add_period_base, info.context.user, project)


class PeriodType(DjangoObjectType):
    """Тип периода."""

    user = graphene.Field(UserType, required=True, description='Пользователь')
    project = graphene.Field(ProjectType, description='Проект')
    methodical_support = DjangoListField(FileType, description='Методическая поддержка')
    divisions = graphene.List(lambda: DivisionModelType, description='Участвующие дивизионы')
    period_groups = graphene.List(lambda: PeriodGroupType, description='Группы пользователей назначенных в сборе')
    sheets = graphene.List(lambda: BaseSheetType, required=True, description='Листы')

    can_add_document = graphene.Boolean(
        required=True,
        description='Может ли пользователь добавлять документы в период'
    )
    can_change_divisions = graphene.Boolean(
        required=True,
        description='Может ли пользователь изменять дивизионы периода'
    )
    can_change_groups = graphene.Boolean(
        required=True,
        description='Может ли пользователь изменять группы периода'
    )
    can_change_users = graphene.Boolean(
        required=True,
        description='Может ли пользователь изменять пользователей периода'
    )
    can_change_settings = graphene.Boolean(
        required=True,
        description='Может ли пользователь изменять настройки периода'
    )
    can_change_sheet = graphene.Boolean(
        required=True,
        description='Может ли пользователь изменять структуру листа периода'
    )
    can_delete = graphene.Boolean(
        required=True,
        description='Может ли пользователь удалять период'
    )

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
        )
        convert_choices_to_enum = False

    @staticmethod
    @resolver_hints(model_field='division_set')
    def resolve_divisions(period: Period, info: ResolveInfo) -> list[dict[str, int | str]]:
        return get_period_divisions(period)

    @staticmethod
    @resolver_hints(model_field='periodgroup_set')
    def resolve_period_groups(period: Period, info: ResolveInfo):
        return period.periodgroup_set.all()

    @staticmethod
    @resolver_hints(model_field='sheet_set')
    def resolve_sheets(period: Period, info: ResolveInfo) -> QuerySet[Sheet]:
        return period.sheet_set.all()

    @staticmethod
    def resolve_can_add_document(period: Period, info: ResolveInfo) -> bool:
        return AddDocumentBase(info.context.user, period).can_add_any_document

    @staticmethod
    def resolve_can_change_divisions(period: Period, info: ResolveInfo) -> bool:
        return not is_raises(PermissionDenied, can_change_period_divisions_base, info.context.user, period)

    @staticmethod
    def resolve_can_change_groups(period: Period, info: ResolveInfo) -> bool:
        return not is_raises(PermissionDenied, can_change_period_groups_base, info.context.user, period)

    @staticmethod
    def resolve_can_change_users(period: Period, info: ResolveInfo) -> bool:
        return not is_raises(PermissionDenied, can_change_period_users_base, info.context.user, period)

    @staticmethod
    def resolve_can_change_settings(period: Period, info: ResolveInfo) -> bool:
        return not is_raises(PermissionDenied, can_change_period_settings_base, info.context.user, period)

    @staticmethod
    def resolve_can_change_sheet(period: Period, info: ResolveInfo) -> bool:
        return not is_raises(PermissionDenied, can_change_period_sheet_base, info.context.user, period)

    @staticmethod
    def resolve_can_delete(period: Period, info: ResolveInfo) -> bool:
        return not is_raises(PermissionDenied, can_delete_period_base, info.context.user, period)


class DivisionModelType(graphene.ObjectType):
    """Описание обобщенного типа дивизиона."""

    id = graphene.ID(required=True, description='Идентификатор модели дивизиона')
    name = graphene.String(required=True, description='Название дивизиона')
    model = graphene.String(required=True, description='Модель дивизиона: department, organization')

    class Meta:
        interfaces = (graphene.relay.Node,)


class DivisionModelTypeConnection(graphene.relay.Connection):
    """Connection для обобщенного типа дивизиона."""

    class Meta:
        node = DivisionModelType


class OrganizationOriginalType(DjangoObjectType):
    """Описание списка организаций."""

    departments = graphene.List(DepartmentType, description='Департаменты')
    users = graphene.List(UserType, description='Пользователи')

    class Meta:
        model = Organization
        fields = (
            'id', 'name', 'present_name',
            'inn', 'kpp', 'kind',
            'rubpnubp', 'kodbuhg', 'okpo',
            'phone', 'site', 'mail', 'address',
            'attributes',
            'created_at', 'updated_at',
            'parent',
            'region',
            'departments'
        )

    @staticmethod
    @resolver_hints(model_field='department_set')
    def resolve_departments(organization: Organization, info: ResolveInfo, *args, **kwargs) -> QuerySet:
        return organization.department_set.all()

    @staticmethod
    @resolver_hints(model_field='')
    def resolve_departments(organization: Organization, info: ResolveInfo, *args, **kwargs) -> QuerySet:
        return organization.users.all()


class PrivilegeType(DjangoObjectType):
    """Описание сквозных привилегий."""

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
    def resolve_users(period_group: PeriodGroup, info: ResolveInfo, *args, **kwargs) -> QuerySet[User]:
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
        fields = ('id', 'name', 'edit', 'protected', 'comment',)


class DocumentType(DjangoObjectType):
    """Тип моделей документа."""

    user = graphene.Field(UserType, description='Пользователь, добавивший документ')
    period = graphene.Field(PeriodType, description='Период сбора')
    sheets = graphene.List(lambda: BaseSheetType, required=True, description='Листы')
    last_status = graphene.Field(lambda: DocumentStatusType, description='Последний статус документа')

    can_change = graphene.Boolean(required=True, description='Может ли пользователь изменять документ')
    can_delete = graphene.Boolean(required=True, description='Может ли пользователь удалять документ')

    object_id = graphene.ID(description='Идентификатор дивизиона')

    class Meta:
        model = Document
        interfaces = (graphene.relay.Node,)
        fields = (
            'id',
            'comment',
            'version',
            'created_at',
            'updated_at',
            'user',
            'period',
            'sheets',
            'object_id',
            'object_name',
            'last_status',
        )
        filterset_class = DocumentFilter
        connection_class = CountableConnection

    @staticmethod
    def resolve_sheets(document: Document, info: ResolveInfo) -> QuerySet[Sheet]:
        return document.sheets.all()

    @staticmethod
    def resolve_can_change(document: Document, info: ResolveInfo) -> bool:
        return not is_raises(PermissionDenied, can_change_document_base, info.context.user, document)


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


class ColumnDimensionType(graphene.ObjectType):
    """Тип колонки."""

    id = graphene.ID(required=True, description='Идентификатор')
    index = graphene.Int(required=True, description='Индекс колонки')
    name = graphene.String(required=True, description='Название колонки')
    width = graphene.Int(description='Ширина колонки')
    fixed = graphene.Boolean(required=True, description='Фиксация колонки')
    hidden = graphene.Boolean(required=True, description='Скрытие колонки')
    kind = graphene.String(required=True, description='Тип значений')
    created_at = graphene.DateTime(required=True, description='Дата добавления')
    updated_at = graphene.DateTime(required=True, description='Дата обновления')
    user_id = graphene.ID(description='Идентификатор пользователя')


class RowDimensionType(graphene.ObjectType):
    """Тип строки."""

    id = graphene.ID(required=True, description='Идентификатор')
    index = graphene.Int(required=True, description='Индекс строки относительно родителя')
    global_index = graphene.Int(required=True, description='Индекс строки в плоской структуре')
    name = graphene.String(required=True, description='Название строки')
    height = graphene.Int(description='Высота строки')
    fixed = graphene.Boolean(required=True, description='Фиксация строки')
    hidden = graphene.Boolean(required=True, description='Скрытие строки')
    dynamic = graphene.Boolean(required=True, description='Динамическая ли строка')
    aggregation = graphene.String(description='Агрегирование перечисление (мин, макс) для динамических строк')
    created_at = graphene.DateTime(required=True, description='Дата добавления')
    updated_at = graphene.DateTime(required=True, description='Дата обновления')
    parent = graphene.Field(lambda: RowDimensionType, description='Родительская строка')
    children = graphene.List(graphene.NonNull(lambda: RowDimensionType), required=True, description='Дочерние строки')
    document_id = graphene.ID(description='Идентификатор документа')
    object_id = graphene.ID(description='Идентификатор дивизиона')
    user_id = graphene.ID(description='Идентификатор пользователя')
    cells = graphene.List(graphene.NonNull(lambda: CellType), required=True, description='Ячейки')


class ChangeColumnDimensionType(DjangoObjectType):
    kind = graphene.String(required=True, description='Тип значений')

    class Meta:
        model = ColumnDimension
        fields = (
            'id',
            'width',
            'fixed',
            'hidden',
            'kind',
            'updated_at',
        )


class ChangeRowDimensionType(DjangoObjectType):
    class Meta:
        model = RowDimension
        fields = (
            'id',
            'height',
            'fixed',
            'hidden',
            'dynamic',
            'updated_at',
        )


class CellType(graphene.ObjectType):
    """Тип ячейки."""

    id = graphene.ID(required=True, description='Идентификатор')
    # apps.dcis.models.KindCell
    kind = graphene.String(required=True, description='Тип значения')

    # apps.dcis.models.Cell
    editable = graphene.Boolean(required=True, description='Редактируемая ячейка')
    formula = graphene.String(description='Формула')
    number_format = graphene.String(description='Форматирование чисел')
    comment = graphene.String(description='Комментарий')
    mask = graphene.String(description='Маска для ввода значений')
    tooltip = graphene.String(description='Подсказка')
    column_id = graphene.ID(description='Идентификатор колонки')
    row_id = graphene.ID(description='Идентификатор строки')

    # apps.dcis.models.Style
    horizontal_align = graphene.ID(description='Горизонтальное выравнивание')
    vertical_align = graphene.ID(description='Вертикальное выравнивание')
    size = graphene.Int(required=True, description='Размер шрифта')
    strong = graphene.Boolean(required=True, description='Жирный шрифт')
    italic = graphene.Boolean(required=True, description='Курсив')
    strike = graphene.Boolean(required=True, description='Зачеркнутый')
    underline = graphene.String(description='Тип подчеркивания')
    color = graphene.String(required=True, description='Цвет индекса')
    background = graphene.String(required=True, description='Цвет фона')
    border_style = graphene.JSONString(required=True, description='Стили границ')
    border_color = graphene.JSONString(required=True, description='Цвет границ')

    # Расчетные значения
    position = graphene.String(required=True, description='Позиция относительно родительской строки')
    global_position = graphene.String(required=True, description='Позиция в плоской структуре')
    related_global_positions = graphene.List(
        graphene.NonNull(graphene.String),
        required=True,
        description='Связанные с объединением позиции в плоской структуре'
    )
    colspan = graphene.Int(required=True, description='Объединение колонок')
    rowspan = graphene.Int(required=True, description='Объединение строк')

    # От Value
    value = graphene.String(description='Значение')
    verified = graphene.Boolean(required=True, description='Валидно ли поле')
    error = graphene.String(description='Текст ошибки')


class ValueType(DjangoObjectType):
    """Тип значения."""

    payload = graphene.String(description='Дополнительное поле')
    document = graphene.Field(DocumentType, description='Документ')
    sheet_id = graphene.ID(required=True, description='Идентификатор листа')
    column_id = graphene.ID(required=True, description='Идентификатор колонки')
    row_id = graphene.ID(required=True, description='Идентификатор строки')

    class Meta:
        model = Value
        fields = (
            'id',
            'value',
            'payload',
            'verified',
            'error',
            'document',
        )

    @staticmethod
    def resolve_payload(value: Value, info: ResolveInfo) -> str:
        return json.dumps(value.payload) if value.payload is not None else None


class BaseSheetType(graphene.ObjectType):
    """Тип листа без структуры."""

    id = graphene.ID(required=True, description='Идентификатор')
    name = graphene.String(required=True, description='Наименование')
    position = graphene.Int(required=True, description='Позиция')
    comment = graphene.String(required=True, description='Комментарий')
    created_at = graphene.DateTime(required=True, description='Дата добавления')
    updated_at = graphene.DateTime(required=True, description='Дата обновления')
    period = graphene.Field(PeriodType, description='Период')


class SheetType(BaseSheetType):
    """Тип листа."""

    columns = graphene.List(graphene.NonNull(lambda: ColumnDimensionType), description='Колонки')
    rows = graphene.List(graphene.NonNull(lambda: RowDimensionType), description='Строки')
    can_change = graphene.Boolean(required=True, description='Может ли пользователь изменять лист')
    can_change_value = graphene.Boolean(required=True, description='Может ли пользователь изменять значение ячейки')
    can_add_child_row_dimension = graphene.Boolean(
        required=True,
        description='Может ли пользователь добавлять дочерние строки для строк'
    )
    can_change_child_row_dimension_height = graphene.Boolean(
        required=True,
        description='Может ли пользователь изменять высоту дочерней строки'
    )
    can_delete_child_row_dimension = graphene.Boolean(
        required=True,
        description='Может ли пользователь удалять дочернюю строку, не имеющую собственных дочерних строк'
    )


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


class ChangedCellOption(graphene.ObjectType):
    """Измененное свойство ячейки."""

    cell_id = graphene.ID(required=True, description='Идентификаторы ячеек')
    field = graphene.String(required=True, description='Идентификатор поля')
    value = graphene.String(description='Значение поля')


class GlobalIndicesInputType(graphene.InputObjectType):
    """Индекс строки в плоской структуре."""

    row_id = graphene.ID(required=True, description='Идентификатор строки')
    global_index = graphene.Int(required=True, description='Индекс в плоской структуре')
