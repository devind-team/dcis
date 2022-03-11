from typing import List
from openpyexcel.utils.cell import get_column_letter
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models import User
from .document import Document, Sheet


class Style(models.Model):
    """Абстрактная модель применяемых стилей для страниц сборов."""

    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'

    KIND_HORIZONTAL_ALIGN = (
        (LEFT, 'left'),
        (CENTER, 'center'),
        (RIGHT, 'right')
    )

    TOP = 0
    BOTTOM = 1
    MIDDLE = 2

    KIND_VERTICAL_ALIGN = (
        (TOP, 'top'),
        (MIDDLE, 'middle'),
        (BOTTOM, 'bottom'),
    )

    SINGLE = 'single'
    DOUBLE = 'double'
    SINGLE_ACCOUNTING = 'single_accounting'
    DOUBLE_ACCOUNTING = 'double_accounting'

    KIND_UNDERLINE = (
        (SINGLE, 'single'),
        (DOUBLE, 'double'),
        (SINGLE_ACCOUNTING, 'single_accounting'),
        (DOUBLE_ACCOUNTING, 'double_accounting')
    )

    horizontal_align = models.CharField(
        max_length=10,
        default=None,
        null=True,
        choices=KIND_HORIZONTAL_ALIGN,
        help_text='Горизонтальное выравнивание'
    )
    vertical_align = models.CharField(
        max_length=10,
        default=None,
        null=True,
        choices=KIND_VERTICAL_ALIGN,
        help_text='Вертикальное выравнивание'
    )
    size = models.PositiveIntegerField(default=12, help_text='Размер шрифта')
    strong = models.BooleanField(default=False, help_text='Жирный шрифт')
    italic = models.BooleanField(default=False, help_text='Курсив')
    strike = models.BooleanField(default=None, null=True, help_text='Зачеркнутый')
    underline = models.CharField(
        max_length=20,
        default=None,
        null=True,
        choices=KIND_UNDERLINE,
        help_text='Тип подчеркивания'
    )
    color = models.CharField(max_length=7, default='#000000', help_text='Цвет индекса')
    background = models.CharField(max_length=7, default='#FFFFFF', help_text='Цвет фона')

    class Meta:
        abstract = True


class SheetDivision(models.Model):
    """Описание обобщенных полей для связи с дивизионом строк и столбцов.

    - user - пользователь, который добавил колонку.
    - content_type - дивизион Department, Organization.
    - object_id - идентификатор дивизиона Department, Organization.
    - content_object - генерация связи к дивизиону.

    При первоначальном заполнении таблицы все поля устанавливаются по умолчанию.
    """

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, help_text='Пользователь')
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class ColumnDimension(Style, SheetDivision, models.Model):
    """Модель стилей для колонки таблицы.

    Ссылка на оригинальный класс из openpyxl:
    https://foss.heptapod.net/openpyxl/openpyxl/-/blob/branch/3.0/openpyxl/worksheet/dimensions.py

    - auto_size - если True, то поле width не имеет значения
    """

    index = models.PositiveIntegerField(help_text='Индекс колонки')
    width = models.PositiveIntegerField(help_text='Ширина колонки')
    fixed = models.BooleanField(default=False, help_text='Фиксация колонки')
    hidden = models.BooleanField(default=False, help_text='Скрытое поле')
    auto_size = models.BooleanField(default=False, help_text='Автоматическая ширина')

    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, help_text='Лист')

    class Meta:
        ordering = ('index', 'id',)
        unique_together = [['index', 'sheet']]


class RowDimension(Style, SheetDivision, models.Model):
    """Модель стилей для строки таблицы.

    Кроме того, что таблица плоская, могут быть еще промежуточные агрегаций,
    они реализуются с помощью дополнительных полей.

    - dynamic - описывает динамическую строку
    - aggregation - способ агрегации дочерних строк (SUM, MIN, MAX, AVG)
    - parent - ссылка на родительскую строку
    - document - ссылка на документ.
        Это поле необходимо для того, чтобы к обычным строкам плоской таблицы
        добавлять динамические строки, которые не относятся к определенному документу,
        однако, должны участвовать при заполнении финальной версии документа.
    """

    SUM = 'SUM'
    MIN = 'MIN'
    MAX = 'MAX'
    AVG = 'AVG'

    KIND_AGGREGATION = (
        (SUM, 'sum'),
        (MIN, 'min'),
        (MAX, 'max'),
        (AVG, 'avg'),
    )

    index = models.PositiveIntegerField(default=0, help_text='Индекс строки')
    height = models.PositiveIntegerField(null=True, help_text='Высота колонки')

    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, help_text='Лист')

    dynamic = models.BooleanField(default=False, help_text='Динамическая ли строка')
    aggregation = models.CharField(
        max_length=3,
        null=True,
        default=None,
        choices=KIND_AGGREGATION,
        help_text='Агрегирование перечисление (мин, макс) для динамических строк'
    )
    parent = models.ForeignKey(
        'self',
        default=None,
        null=True,
        on_delete=models.CASCADE,
        help_text='Родительское правило'
    )
    document = models.ForeignKey(
        Document,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        help_text='Документ, для динамических строк'
    )

    class Meta:
        ordering = ('index', 'id',)


class Cell(Style, models.Model):
    """Модель ячейки."""

    # Формат из openpyxl
    NUMERIC = 'n'
    STRING = 's'
    FORMULA = 'f'
    BOOL = 'b'
    INLINE = 'inlineStr'
    ERROR = 'e'
    FORMULA_CACHE_STRING = 'str'
    DATE = 'd'

    # Дополнительный набор
    FILE = 'fl'

    KIND_VALUE = (
        (NUMERIC, 'n'),
        (STRING, 's'),
        (FORMULA, 'f'),
        (BOOL, 'b'),
        (INLINE, 'inlineStr'),
        (ERROR, 'e'),
        (FORMULA_CACHE_STRING, 'str'),
        (DATE, 'd'),
        (FILE, 'fl'),
    )

    kind = models.PositiveIntegerField(default=NUMERIC, choices=KIND_VALUE, help_text='Тип значения')
    formula = models.TextField(null=True, help_text='Формула')
    comment = models.TextField(null=True, help_text='Комментарий')
    default = models.TextField(null=True, help_text='Значение по умолчанию')
    mask = models.TextField(null=True, help_text='Маска для ввода значений')
    tooltip = models.TextField(null=True, help_text='Подсказка')

    column = models.ForeignKey(ColumnDimension, on_delete=models.CASCADE, help_text='Колонка')
    row = models.ForeignKey(RowDimension, on_delete=models.CASCADE, help_text='Строка')

    class Meta:
        unique_together = (('column', 'row'),)
        indexes = [models.Index(fields=['column', 'row'])]


class Limitation(models.Model):
    """Накладываемые на ячейку ограничения."""

    AND = 'AND'
    OR = 'OR'

    KIND_OPERATOR = (
        (AND, 'and'),
        (OR, 'or')
    )

    LT = 0
    GT = 1
    EQUAL = 2
    LTE = 3
    GTE = 4

    KIND_CONDITION = (
        (LT, '<'),
        (GT, '>'),
        (EQUAL, '='),
        (LTE, '<='),
        (GTE, '>=')
    )
    operator = models.CharField(max_length=3, default=AND, choices=KIND_OPERATOR, help_text='Оператор')
    condition = models.PositiveIntegerField(default=EQUAL, choices=KIND_CONDITION, help_text='Состояние')
    value = models.TextField(help_text='Значение')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, help_text='Родительское правило')
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, help_text='Ячейка')


class MergedCell(models.Model):
    """Модель объединенной ячейки."""

    min_col = models.IntegerField(help_text='Начальная позиция в колонке')
    min_row = models.IntegerField(help_text='Начальная позиция в строке')
    max_col = models.IntegerField(help_text='Конечная позиция в колонке')
    max_row = models.IntegerField(help_text='Конечная позиция в строке')

    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, help_text='Лист')

    class Meta:
        unique_together = [['min_col', 'min_row', 'sheet']]

    def __str__(self) -> str:
        return f'{get_column_letter(self.min_col)}{self.min_row}:' \
               f'{get_column_letter(self.max_col)}{self.max_row}'

    @property
    def colspan(self) -> int:
        return self.max_col - self.min_col + 1

    @property
    def rowspan(self) -> int:
        return self.max_row - self.min_row + 1

    @property
    def target(self) -> str:
        return f'{get_column_letter(self.min_col)}{self.min_row}'

    @property
    def cells(self) -> List[str]:
        not_cell: List[str] = []
        for col in range(self.min_col, self.max_col + 1):
            for row in range(self.min_row, self.max_row + 1):
                if col == 1 and row == 1:
                    continue
                not_cell.append(f'{get_column_letter(col)}{row}')
        return not_cell


class Value(models.Model):
    """Модель значения поля таблицы.

    Привязка значения осуществляется к дивизиону через документ,
    но в документе может быть несколько листов.
    В связи с этим добавлено поле sheet, которое точно определяет к какому листу имеет отношение таблицы.
    """

    value = models.TextField(help_text='Значение')
    verified = models.BooleanField(default=True, help_text='Валидно ли поле')
    error = models.CharField(max_length=255, null=True, help_text='Текст ошибки')

    document = models.ForeignKey(Document, on_delete=models.CASCADE, help_text='Документ')
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, help_text='Лист')
    column = models.ForeignKey(ColumnDimension, on_delete=models.CASCADE, help_text='Колонка')
    row = models.ForeignKey(RowDimension, on_delete=models.CASCADE, help_text='Строка')

    class Meta:
        indexes = [
            models.Index(fields=['document', 'sheet']),
            models.Index(fields=['document', 'sheet', 'column', 'row'])
        ]
