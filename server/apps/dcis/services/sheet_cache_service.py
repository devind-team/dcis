"""Модуль хранения зависимостей для расчета формул при изменении значений.

При изменении значения ячейки необходимо пересчитывать значение ячейки и всех связных.
Каждый раз вытаскивать все ячейки не целесообразно, можно вытаскивать только связные.


+-----+--------------+--------------+--------------+-------------+
|  #  |  Параметр    | Показатель А | Показатель Б |    Сумма    |
+-----+--------------+--------------+--------------+-------------+
|  #  |  Параметр 1  |      30      |       5      |   =С2 + D2  |
+-----+--------------+--------------+--------------+-------------+
|  #  |  Параметр 2  |      40      |       7      |   =С3 + D3  |
+-----+--------------+--------------+--------------+-------------+
|  #  |  Параметр 3  |      50      |       9      |   =С4 + D4  |
+-----+--------------+--------------+--------------+-------------+
|                                           Итого: | =SUM(E2:E4) |
+-----+--------------+--------------+--------------+-------------+

При изменении ячейки C2 30 -> 40 идет пересчет ячеек:
- E2
- E5

По итогу мы изменяем значения С2, E2, E5.
Формулы работают только на 1 уровне, где parent_id == None.

Используем django адаптер: https://docs.djangoproject.com/en/4.0/topics/cache/
"""

from typing import Optional
from dataclasses import dataclass, asdict, field
from collections import Counter, defaultdict

from xlsx_evaluate.parser import FormulaParser
from xlsx_evaluate.functions.xl import flatten
from xlsx_evaluate.utils import resolve_ranges

from django.core.cache import cache
from jsonpickle import encode, decode


KEY_TEMPLATE = 'cache.sheet.%s'


@dataclass
class FormulaDependencyCache:
    """Структура для хранения кеша.

        - sheet_name - название листа
        - sheet_id - идентификатор листа в БД
        - dependency - частотная зависимость. Какие значения нужно получить, чтобы посчитать значение.
        - inversion - инверсивная зависимость. Какие ячейки нужно посчитать, если изменяется выбранная
    """
    sheet_name: str

    sheet_id: Optional[int] = None

    dependency: dict[str, dict[str, int]] = field(default_factory=lambda: defaultdict(dict))
    inversion: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))

    @property
    def key(self) -> str:
        return KEY_TEMPLATE % self.sheet_id


def save_to_cache(formula_dependency: FormulaDependencyCache):
    """Сохраняем структуру зависимостей в кеш."""
    cache.set(formula_dependency.key, encode(formula_dependency))


def get_from_cache(sheet_id: int) -> Optional[FormulaDependencyCache]:
    """Забираем структуру из кеша."""
    result = cache.get(KEY_TEMPLATE % sheet_id)
    return None if result is None else decode(result)


class FormulaContainerCache:
    """Контейнер для упрощения работы с кешом."""

    def __init__(self, name: str):
        self.sheet_dependency = FormulaDependencyCache(name)

    @property
    def sheet_name(self) -> str:
        return self.sheet_dependency.sheet_name

    @sheet_name.setter
    def sheet_name(self, value: str) -> None:
        self.sheet_dependency.sheet_name = value

    @property
    def sheet_id(self) -> Optional[int]:
        return self.sheet_dependency.sheet_id

    @sheet_id.setter
    def sheet_id(self, value: Optional[int]):
        self.sheet_dependency.sheet_id = value

    def add_formula(self, coordinate: str, formula: str):
        """
        Добавление информации в зависимость
        :param coordinate: координата ячейки
        :param formula: формула
        :return:
        """
        tokens = FormulaParser().tokenize(formula)
        range_tokens = [token for token in tokens if token.tsubtype == 'range']
        dependency = flatten([flatten(resolve_ranges(token.tvalue, '')[1]) for token in range_tokens])
        self.sheet_dependency.dependency[coordinate] = Counter(dependency)
        for coord in set(dependency):
            self.sheet_dependency.inversion[coord].append(coordinate)

    def save(self, sheet_id: Optional[int] = None):
        if sheet_id is not None:
            self.sheet_id = sheet_id
        return save_to_cache(self.sheet_dependency)

    @classmethod
    def from_cache(cls, sheet_id: int):
        result = get_from_cache(sheet_id)
        if result is None:
            return None
        container = cls(result.sheet_name)
        container.sheet_dependency = result
        return container
