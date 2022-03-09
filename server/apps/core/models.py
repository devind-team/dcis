"""Переопределенная пользовательская модель"""

from devind_core.models import AbstractUser
from devind_helpers.relations import get_children


class User(AbstractUser):
    """Переопределенная модель хранения пользователей."""
    pass
