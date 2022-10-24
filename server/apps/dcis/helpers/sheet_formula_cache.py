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
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import ClassVar, Optional, Sequence

from openpyxl.utils.cell import get_column_letter

from apps.dcis.helpers.formula_cache import FormulaContainerCache, FormulaDependencyCache
from apps.dcis.models import Cell, Sheet


@dataclass
class SheetFormulaDependencyCache(FormulaDependencyCache):
    """Кеш для хранения зависимостей формул листа.

        - sheet_name - название листа
        - sheet_id - идентификатор листа в БД
        - dependency - частотная зависимость. Какие значения нужно получить, чтобы посчитать значение.
        - inversion - инверсивная зависимость. Какие ячейки нужно посчитать, если изменяется выбранная.
    """
    KEY_TEMPLATE: ClassVar[str] = 'cache.sheet.formula.%s'

    sheet_name: str
    sheet_id: int | None = None
    dependency: dict[str, dict[str, int]] = field(default_factory=lambda: defaultdict(dict))
    inversion: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))

    @property
    def key(self) -> str:
        return self.KEY_TEMPLATE % self.sheet_id


class SheetFormulaContainerCache(FormulaContainerCache):
    """Контейнер для кеша зависимостей формул листа."""

    def __init__(self, name: str, sheet_id: int | None = None) -> None:
        self.sheet_dependency_cache = SheetFormulaDependencyCache(name)
        self.sheet_id = sheet_id

    @property
    def dependency_cache(self) -> FormulaDependencyCache:
        return self.sheet_dependency_cache

    def transform_dependency(self, dependency: str) -> str:
        if '!' in dependency:
            sheet_name, coordinate = dependency.split('!')
            if sheet_name == self.sheet_name:
                return coordinate
        return dependency

    @property
    def sheet_name(self) -> str:
        return self.sheet_dependency_cache.sheet_name

    @sheet_name.setter
    def sheet_name(self, value: str) -> None:
        self.sheet_dependency_cache.sheet_name = value

    @property
    def sheet_id(self) -> int | None:
        return self.sheet_dependency_cache.sheet_id

    @sheet_id.setter
    def sheet_id(self, value: int | None) -> None:
        self.sheet_dependency_cache.sheet_id = value

    def save(self, sheet_id: int | None = None) -> bool:
        """Сохранение контейнера в кеш."""
        if sheet_id is not None:
            self.sheet_id = sheet_id
        return self.sheet_dependency_cache.save()

    @classmethod
    def get(cls, sheet: Sheet) -> 'SheetFormulaContainerCache':
        """Получение контейнера из кеша или построение нового."""
        container = cls.from_cache(sheet.pk)
        return container if container is not None else cls.build_cache(sheet)

    def delete(self) -> bool:
        """Удаление контейнера из кеша."""
        assert self.sheet_id is not None, 'Невозможно удалить контейнер без идентификатор'
        return SheetFormulaDependencyCache.delete(self.sheet_id)

    @classmethod
    def update(cls, sheet: Sheet) -> Optional['SheetFormulaContainerCache']:
        """Обновление контейнера, если он есть в кеше."""
        container = cls.from_cache(sheet.pk)
        if container is None:
            return container
        container.delete()
        return cls.build_cache(sheet)

    @classmethod
    def from_cache(cls, sheet_id: int) -> Optional['SheetFormulaContainerCache']:
        """Получение контейнера из кеша."""
        result = SheetFormulaDependencyCache.get(sheet_id)
        if result is None:
            return None
        container = cls(result.sheet_name)
        container.sheet_dependency_cache = result
        return container

    @classmethod
    def build_cache(cls, sheet: Sheet) -> 'SheetFormulaContainerCache':
        """Построение нового контейнера."""
        cells: Sequence[Cell] = Cell.objects.filter(
            formula__isnull=False,
            formula__istartswith='=',
            row__parent__isnull=True,
            row__sheet=sheet,
        ).select_related('row', 'column').all()
        container = cls(sheet.name)
        for cell in cells:
            container.add_formula(f'{get_column_letter(cell.column.index)}{cell.row.index}', cell.formula)
        container.save(sheet.pk)
        return container
