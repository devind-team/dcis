"""Модуль для сервисов атрибутов."""

from typing import Sequence, cast

from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.template import Context, Template

from apps.core.models import User
from apps.dcis.models import Attribute, AttributeValue, Cell, Document, Value
from apps.dcis.permissions import can_change_attribute_value
from .value_services import UpdateOrCrateValuesResult, update_or_create_value


def change_attribute_value(
    user: User,
    attribute: Attribute,
    document: Document,
    value: str
) -> tuple[AttributeValue, Sequence[Value]]:
    """Сервис изменения значений атрибута.

    Кроме этого, необходимо собрать контекст из существующих атрибутов и перерендерить.
    """
    try:
        can_change_attribute_value(user, document, attribute)
    except PermissionDenied as error:
        raise PermissionDenied({'value': str(error)})

    attribute_value, _ = AttributeValue.objects.update_or_create(
        document=document,
        attribute=attribute, defaults={
            'value': value
        }
    )
    context: Context = create_attribute_context(user, document)
    values: Sequence[Value] = rerender_values(document, context)
    return attribute_value, values


def rerender_values(document: Document, context: Context) -> Sequence[Value]:
    """Функция для ререндера параметров."""
    sheet_ids = document.sheets.values_list('id', flat=True)
    cell_values: QuerySet[Cell] = Cell.objects.filter(
        is_template=True,
        column__sheet__in=sheet_ids,
        row__sheet__in=sheet_ids
    ).select_related('column').all()
    values: list[Value] = []
    for cell_value in cell_values:
        value = Template(cell_value.default).render(context)
        changed_values: UpdateOrCrateValuesResult = update_or_create_value(
            document,
            cell_value,
            cast(int, cell_value.column.sheet_id),
            value
        )
        values.append(*changed_values.values)
    return values


def create_attribute_context(user: User, document: Document) -> Context:
    """Функция для создания контекста."""
    attributes: QuerySet[Attribute] = Attribute.objects.filter(period=document.period).all()
    attribute_values: dict[int, str] = {
        attribute_value['attribute_id']: attribute_value['value']
        for attribute_value in AttributeValue.objects.filter(document=document).values('attribute_id', 'value')
    }
    context: dict[str, str] = {
        attribute.key: attribute_values.get(attribute.id, attribute.default)
        for attribute in attributes
    }
    # Расширяем контекст с помощью встроенных переменных
    context.update({
        'user': user.get_full_name,
        'org_id': document.object_id,
        'org_name': document.object_name
    })
    return Context(context)
