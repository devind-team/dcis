"""Модуль с кешем для расчета формул."""
from abc import ABC, abstractmethod
from collections import Counter, defaultdict

from xlsx_evaluate.functions.xl import flatten
from xlsx_evaluate.parser import FormulaParser
from xlsx_evaluate.utils import resolve_ranges

from apps.dcis.helpers.cache import Cache


class FormulaDependencyCache(Cache, ABC):
    """Кеш для хранения зависимостей формул.

        - dependency - частотная зависимость. Какие значения нужно получить, чтобы посчитать значение.
        - inversion - инверсивная зависимость. Какие ячейки нужно посчитать, если изменяется выбранная.
    """
    dependency: dict[str, dict[str, int]]
    inversion: dict[str, list[str]]


class FormulaContainerCache(ABC):
    """Контейнер для кеша зависимостей формул."""

    @property
    @abstractmethod
    def dependency_cache(self) -> FormulaDependencyCache:
        """Получение кеша зависимостей формул."""
        ...

    @abstractmethod
    def transform_dependency(self, dependency: str) -> str:
        """Преобразование зависимости."""
        ...

    @property
    def dependency(self) -> dict[str, dict[str, int]]:
        """Частотная зависимость."""
        return self.dependency_cache.dependency

    @property
    def inversion(self) -> dict[str, list[str]]:
        """Инверсивная зависимость."""
        return self.dependency_cache.inversion

    def add_formula(self, coordinate: str, formula: str) -> 'FormulaContainerCache':
        """Добавление информации о формуле.
        :param coordinate: координата ячейки
        :param formula: формула
        :return: текущий контейнер для кеша зависимостей формул
        """
        dependency: list[str] = []
        for dep in self.dependency_formula(formula):
            added_dependency = self.transform_dependency(dep)
            # Мы не должны ссылаться сами на себя.
            if added_dependency != coordinate:
                dependency.append(added_dependency)
        self.dependency_cache.dependency[coordinate] = Counter(dependency)
        for coord in set(dependency):
            self.dependency_cache.inversion[coord].append(coordinate)
        return self

    def delete_formula(self, coordinate: str) -> 'FormulaContainerCache':
        """Удаление информации о формуле.
        :param coordinate: координата ячейки
        :return: текущий контейнер для кеша зависимостей формул
        """
        self.dependency_cache.dependency = {
            coord: counter for coord, counter in self.dependency_cache.dependency if coord != coordinate
        }
        inversion: dict[str, list[str]] = defaultdict(list)
        for ic, iv in self.dependency_cache.inversion.items():
            inversion_clean = [value for value in iv if value != coordinate]
            if inversion_clean:
                inversion[ic] = inversion_clean
        self.dependency_cache.inversion = inversion
        return self

    def change_formula(self, coordinate: str, formula: str) -> 'FormulaContainerCache':
        """Изменение информации о формуле.
        :param coordinate: координата ячейки
        :param formula: формула
        :return: текущий контейнер для кеша зависимостей формул
        """
        return self.delete_formula(coordinate).add_formula(coordinate, formula)

    @staticmethod
    def dependency_formula(formula: str) -> list[str]:
        """Возвращает зависимость токенов."""
        tokens = FormulaParser().tokenize(formula)
        range_tokens = [token for token in tokens if token.tsubtype == 'range']
        return flatten([flatten(resolve_ranges(token.tvalue, '')[1]) for token in range_tokens])
