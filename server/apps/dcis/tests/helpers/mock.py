"""Вспомогательный функции для подмены."""

from contextlib import contextmanager
from typing import Any, Generator
from unittest.mock import patch

from django.db.models import Model


@contextmanager
def patch_db_object(target: Model, attribute: str, new: Any) -> Generator[None, Any, None]:
    """Подмена свойства у модели с сохранением в базу данных."""
    with patch.object(target, attribute, new) as mock:
        target.save(update_fields=(attribute,))
        yield mock
    target.save(update_fields=(attribute,))
