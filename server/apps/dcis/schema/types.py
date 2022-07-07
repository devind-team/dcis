import json

import graphene
from devind_core.schema.types import ContentTypeType, FileType
from devind_dictionaries.models import Organization
from devind_dictionaries.schema import DepartmentType
from devind_helpers.optimized import OptimizedDjangoObjectType
from devind_helpers.schema.connections import CountableConnection
from django.db.models import QuerySet
from graphene_django import DjangoListField, DjangoObjectType
from graphene_django_optimizer import resolver_hints
from graphql import ResolveInfo
from stringcase import snakecase

from apps.core.models import User
from apps.core.schema import UserType
from apps.dcis.helpers.info_fields import get_fields
from apps.dcis.models import (
    Attribute, AttributeValue, Division,
    Document, DocumentStatus, Limitation,
    Period, PeriodGroup, PeriodPrivilege,
    Privilege, Project, Status, Value,
)
from apps.dcis.permissions import (
    AddDocument,
    AddPeriod,
    ChangePeriodDivisions,
    ChangePeriodSettings,
    ChangePeriodSheet,
    ChangePeriodUsers,
    ChangeProject,
    DeletePeriod,
    DeleteProject,
    ChangeDocument,
    DeleteDocument
)
from apps.dcis.services.sheet_unload_services import SheetUploader


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
        return ChangeProject.has_object_permission(info.context, project)

    @staticmethod
    def resolve_can_delete(project: Project, info: ResolveInfo) -> bool:
        return DeleteProject.has_object_permission(info.context, project)

    @staticmethod
    def resolve_can_add_period(project: Project, info: ResolveInfo) -> bool:
        return AddPeriod.has_object_permission(info.context, project)


class PeriodType(DjangoObjectType):
    """Тип периода."""

    user = graphene.Field(UserType, required=True, description='Пользователь')
    project = graphene.Field(ProjectType, description='Проект')
    methodical_support = DjangoListField(FileType, description='Методическая поддержка')
    divisions = graphene.List(lambda: DivisionType, description='Участвующие дивизионы')
    period_groups = graphene.List(lambda: PeriodGroupType, description='Группы пользователей назначенных в сборе')

    can_change_divisions = graphene.Boolean(
        required=True,
        description='Может ли пользователь изменять дивизионы периода'
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
    can_add_document = graphene.Boolean(
        required=True,
        description='Может ли пользователь добавлять документы в период'
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
            'period_groups',
            'project',
            'methodical_support'
        )
        convert_choices_to_enum = False

    @staticmethod
    @resolver_hints(model_field='')
    def resolve_divisions(period: Period, info: ResolveInfo, *args, **kwargs):
        return period.division_set.all()

    @staticmethod
    @resolver_hints(model_field='')
    def resolve_period_groups(period: Period, info: ResolveInfo, *args, **kwargs):
        return period.periodgroup_set.all()

    @staticmethod
    def resolve_can_change_divisions(period: Period, info: ResolveInfo) -> bool:
        return ChangePeriodDivisions.has_object_permission(info.context, period)

    @staticmethod
    def resolve_can_change_users(period: Period, info: ResolveInfo) -> bool:
        return ChangePeriodUsers.has_object_permission(info.context, period)

    @staticmethod
    def resolve_can_change_settings(period: Period, info: ResolveInfo) -> bool:
        return ChangePeriodSettings.has_object_permission(info.context, period)

    @staticmethod
    def resolve_can_change_sheet(period: Period, info: ResolveInfo) -> bool:
        return ChangePeriodSheet.has_object_permission(info.context, period)

    @staticmethod
    def resolve_can_delete(period: Period, info: ResolveInfo) -> bool:
        return DeletePeriod.has_object_permission(info.context, period)

    @staticmethod
    def resolve_can_add_document(period: Period, info: ResolveInfo) -> bool:
        return AddDocument.has_object_permission(info.context, period)


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
    name = graphene.String(required=True, description='Название дивизиона')
    model = graphene.String(required=True, description='Модель дивизиона: department, organization')


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
        fields = ('id', 'name', 'edit', 'comment',)


class DocumentType(DjangoObjectType):
    """Тип моделей документа."""

    period = graphene.Field(PeriodType, description='Период сбора')
    sheets = graphene.List(lambda: SheetType, required=True, description='Листы')
    last_status = graphene.Field(lambda: DocumentStatusType, description='Последний статус документа')

    can_change = graphene.Boolean(required=True, description='Может ли пользователь изменять документ')
    can_delete = graphene.Boolean(required=True, description='Может ли пользователь удалять документ')

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
    def resolve_sheets(document: Document, info: ResolveInfo) -> list[dict] | dict:
        return [
            SheetUploader(
                sheet=sheet,
                fields=[snakecase(k) for k in get_fields(info).keys() if k != '__typename'],
                document_id=document.id
            ).unload()
            for sheet in document.sheets.all()
        ]

    @staticmethod
    def resolve_last_status(document: Document, info: ResolveInfo) -> DocumentStatus | None:
        try:
            return document.documentstatus_set.latest('created_at')
        except DocumentStatus.DoesNotExist:
            return None

    @staticmethod
    def resolve_can_change(document: Document, info: ResolveInfo) -> bool:
        return ChangeDocument.has_object_permission(info.context, document)

    @staticmethod
    def resolve_can_delete(document: Document, info: ResolveInfo) -> bool:
        return DeleteDocument.has_object_permission(info.context, document)


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
    user = graphene.List(UserType, description='Пользователь')


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
    user = graphene.List(UserType, description='Пользователь')
    cells = graphene.List(graphene.NonNull(lambda: CellType), required=True, description='Ячейки')


class CellType(graphene.ObjectType):
    """Тип ячейки."""

    id = graphene.Int(required=True, description='Идентификатор')
    # apps.dcis.models.KindCell
    kind = graphene.String(required=True, description='Тип значения')

    # apps.dcis.models.Cell
    editable = graphene.Boolean(required=True, description='Редактируемая ячейка')
    formula = graphene.String(description='Формула')
    comment = graphene.String(description='Комментарий')
    mask = graphene.String(description='Маска для ввода значений')
    tooltip = graphene.String(description='Подсказка')
    column_id = graphene.ID(description='Идентификатор колонки')
    row_id = graphene.ID(description='Идентификатор строки')
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
    """Тип значений"""
    document = graphene.Field(DocumentType, description='Документ')
    payload = graphene.String(description='Дополнительное поле')
    sheet_id = graphene.Int(required=True, description='Идентификатор листа')
    column_id = graphene.Int(required=True, description='Идентификатор колонки')
    row_id = graphene.Int(required=True, description='Идентификатор строки')

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


class SheetType(graphene.ObjectType):
    """Тип листа."""

    id = graphene.Int(required=True, description='Идентификатор')
    name = graphene.String(required=True, description='Наименование')
    position = graphene.Int(required=True, description='Позиция')
    comment = graphene.String(required=True, description='Комментарий')
    created_at = graphene.DateTime(required=True, description='Дата добавления')
    updated_at = graphene.DateTime(required=True, description='Дата обновления')
    period = graphene.Field(PeriodType, description='Период')
    columns = graphene.List(lambda: ColumnDimensionType, description='Колонки')
    rows = graphene.List(lambda: RowDimensionType, description='Строки')


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
