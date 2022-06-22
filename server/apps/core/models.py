"""Переопределение моделей приложения core."""

from devind_core.models import AbstractUser


class User(AbstractUser):
    """Переопределенная модель хранения пользователей."""

    pass
