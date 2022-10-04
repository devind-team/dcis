"""Модуль для сервисов атрибутов."""

from typing import Sequence

from apps.dcis.models import Period, Attribute, Document, AttributeValue, Value
from apps.core.models import User
from apps.dcis.permissions import can_change_period_attributes


def add_attribute(period: Period):
    pass


def delete_attribute(user: User, attribute: Attribute):
    """Удаление атрибута."""
    can_change_period_attributes(user, attribute.period)
    attribute.delete()


def change_attribute_value(
    user: User,
    attribute: Attribute,
    document: Document,
    value: str
) -> tuple[AttributeValue, Sequence[Value]]:
    """Сервис изменения значений атрибута.

    Кроме этого, необходимо собрать контекст из существующих атрибутов и перерендерить.
    """
    # TODO: Роман, нужно на примере изменений ячейки изменить пермишен на атрибут
    # try:
    #     can_change_value(info.context.user, document, attribute)
    # except PermissionDenied as e:
    #     # todo: на strawberry это будет raise PermissionDenied({'value': str(e)})
    #     return ChangeAttributeValueMutation(success=False, errors=[ErrorFieldType('value', [str(e)])])

    attribute_value: AttributeValue = AttributeValue.objects.update_or_create(document=document, attribute=attribute, defaults={
        'value': value
    })

    return attribute_value, []
