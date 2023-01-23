"""Модель с оберткой для кеша: https://docs.djangoproject.com/en/4.0/topics/cache/."""
from abc import ABC, abstractmethod
from typing import ClassVar, Union

from django.core.cache import cache
from jsonpickle import decode, encode


class Cache(ABC):
    """Обертка для работы с кешем."""
    KEY_TEMPLATE: ClassVar[str] = ''

    @property
    @abstractmethod
    def key(self) -> str:
        """Ключ кеша."""
        ...

    def save(self) -> bool:
        """Сохраняем структуру в кеш."""
        return cache.set(self.key, encode(self))

    @classmethod
    def get(cls, object_id: int | str) -> Union['Cache', None]:
        """Забираем структуру из кеша."""
        result = cache.get(cls.KEY_TEMPLATE % object_id)
        return None if result is None else decode(result)

    @classmethod
    def delete(cls, object_id: int | str) -> bool:
        """Удаление структуры из кеша."""
        return cache.delete(cls.KEY_TEMPLATE % object_id)
