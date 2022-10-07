"""Модуль для сервисов атрибутов."""

from typing import Sequence

from django.core.exceptions import PermissionDenied
from apps.core.models import User
from apps.dcis.models import Period, Attribute, Document, AttributeValue, Value
from apps.dcis.permissions import can_change_period_attributes


def add_attribute(period: Period):
    pass


def delete_attribute(user: User, attribute: Attribute):
    """Удаление атрибута."""
    can_change_period_attributes(user, attribute.period)
    attribute.delete()


def change_attribute_value(
    user: User,
    period: Period,
    attribute: Attribute,
    document: Document,
    value: str
) -> tuple[AttributeValue, Sequence[Value]]:
    """Сервис изменения значений атрибута.

    Кроме этого, необходимо собрать контекст из существующих атрибутов и перерендерить.
    """
    try:
        can_change_period_attributes(user, period)
    except PermissionDenied as error:
        raise PermissionDenied({'value': str(error)})

    attribute_value, created = AttributeValue.objects.update_or_create(
        document=document,
        attribute=attribute, defaults={
            'value': value
        }
    )

    return attribute_value, []
