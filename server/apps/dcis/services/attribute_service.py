"""Модуль для сервисов атрибутов."""


from apps.dcis.models import Period, Attribute
from apps.core.models import User
from apps.dcis.permissions import can_change_period_attributes


def add_attribute(period: Period):
    pass


def delete_attribute(user: User, attribute: Attribute):
    """Удаление атрибута."""
    can_change_period_attributes(user, attribute.period)
    attribute.delete()
