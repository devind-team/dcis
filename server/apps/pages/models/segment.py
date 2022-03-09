from django.conf import settings
from django.db import models

from .page_kind import PageKind


class Segment(models.Model):
    """Сегмент (блок) составной страницы"""

    LEFT = 0
    CENTER = 1
    RIGHT = 2

    KIND_ALIGN = (
        (LEFT, 'Left'),
        (CENTER, 'Center'),
        (RIGHT, 'Right')
    )

    EMPTY_VIEW = 0
    CARD_VIEW = 1

    KIND_VIEW = (
        (EMPTY_VIEW, 'empty'),
        (CARD_VIEW, 'card')
    )

    name = models.CharField(max_length=255, null=True, help_text='Заголовок страницы')
    align = models.PositiveIntegerField(choices=KIND_ALIGN, default=LEFT, help_text='Выравнивание заголовка')
    view = models.PositiveIntegerField(choices=KIND_VIEW, null=True, help_text='Тип элемента для рендера')
    position = models.PositiveIntegerField(default=0, help_text='Позиция в сортировке')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    class Meta:
        ordering = ('position',)


class SegmentElement(models.Model):
    """Элемент сегмента"""

    EMPTY_VIEW = 0
    CARD_VIEW = 1

    KIND_VIEW = (
        (EMPTY_VIEW, 'empty'),
        (CARD_VIEW, 'card')
    )

    GRID_REPRESENT = 0
    CARD_REPRESENT = 1
    LIST_REPRESENT = 2
    SLIDER_REPRESENT = 3

    KIND_REPRESENT = (
        (GRID_REPRESENT, 'grid'),
        (CARD_REPRESENT, 'card'),
        (LIST_REPRESENT, 'list'),
        (SLIDER_REPRESENT, 'slider')
    )

    view = models.PositiveIntegerField(choices=KIND_VIEW, null=True, help_text='Тип элемента для рендера')
    represent = models.PositiveIntegerField(choices=KIND_REPRESENT, null=True, help_text='Представление')
    columns = models.PositiveIntegerField(default=1, help_text='Колонок в элементе')
    width = models.PositiveIntegerField(default=12, help_text='Ширина колонки')
    page_size = models.PositiveIntegerField(default=12, help_text='Количество страниц в запросе')
    position = models.PositiveIntegerField(default=0, help_text='Позиция в сортировке')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, help_text='Сегмент страницы')
    page_kind = models.ForeignKey(PageKind, on_delete=models.CASCADE, help_text='Тип привязанной страницы')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, help_text='Пользователь')

    class Meta:
        ordering = ('position',)
