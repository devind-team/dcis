"""Модуль хранения зависимостей для расчета формул ограничений."""
from collections import defaultdict
from dataclasses import dataclass, field
from typing import ClassVar, Optional

from apps.dcis.helpers.formula_cache import FormulaContainerCache, FormulaDependencyCache
from apps.dcis.models import Limitation, Period


@dataclass
class LimitationFormulaDependencyCache(FormulaDependencyCache):
    """Кеш для хранения зависимостей формул ограничений.

        - period_id - идентификатор периода в БД
        - dependency - частотная зависимость. Какие значения нужно получить, чтобы посчитать значение.
        - inversion - инверсивная зависимость. Какие ячейки нужно посчитать, если изменяется выбранная.
    """
    KEY_TEMPLATE: ClassVar[str] = 'cache.limitation.formula.%s'

    period_id: int | None = None
    dependency: dict[str, dict[str, int]] = field(default_factory=lambda: defaultdict(dict))
    inversion: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))

    @property
    def key(self) -> str:
        return self.KEY_TEMPLATE % self.period_id


class LimitationFormulaContainerCache(FormulaContainerCache):
    """Контейнер для кеша зависимостей формул ограничений."""

    def __init__(self, period_id: int | None = None) -> None:
        self.limitation_dependency_cache = LimitationFormulaDependencyCache()
        self.period_id = period_id

    @property
    def dependency_cache(self) -> FormulaDependencyCache:
        return self.limitation_dependency_cache

    def transform_dependency(self, dependency: str) -> str:
        return dependency

    @property
    def period_id(self) -> int | None:
        return self.limitation_dependency_cache.period_id

    @period_id.setter
    def period_id(self, value: int | None) -> None:
        self.limitation_dependency_cache.period_id = value

    def save(self, period_id: int | None = None) -> bool:
        """Сохранение контейнера в кеш."""
        if period_id is not None:
            self.period_id = period_id
        return self.limitation_dependency_cache.save()

    @classmethod
    def get(cls, period: Period) -> 'LimitationFormulaContainerCache':
        """Получение контейнера из кеша или построение нового."""
        container = cls.from_cache(period.pk)
        return container if container is not None else cls.build_cache(period)

    def delete(self) -> bool:
        """Удаление контейнера из кеша."""
        assert self.period_id is not None, 'Невозможно удалить контейнер без идентификатор'
        return LimitationFormulaDependencyCache.delete(self.period_id)

    @classmethod
    def update(cls, period: Period) -> Optional['LimitationFormulaContainerCache']:
        """Обновление контейнера, если он есть в кеше."""
        container = cls.from_cache(period.pk)
        if container is None:
            return container
        container.delete()
        return cls.build_cache(period)

    @classmethod
    def from_cache(cls, period_id: int) -> Optional['LimitationFormulaContainerCache']:
        """Получение контейнера из кеша."""
        cache = LimitationFormulaDependencyCache.get(period_id)
        if cache is None:
            return None
        container = cls()
        container.limitation_dependency_cache = cache
        return container

    @classmethod
    def build_cache(cls, period: Period) -> 'LimitationFormulaContainerCache':
        """Построение нового контейнера."""
        limitations = Limitation.objects.filter(sheet__in=period.sheet_set.all())
        container = cls()
        for i, limitation in enumerate(limitations, 1):
            container.add_formula(f'A{i}', limitation.formula)
        container.save(period.id)
        return container
