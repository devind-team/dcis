from django.conf import settings
from django.db import models

from devind_helpers.resolve_model import ResolveModel
from .page import Page


class Section(models.Model, ResolveModel):
    """Секция"""

    TEXT = 0
    GALLERY = 1
    FILES = 2
    USERS = 3
    SLIDERS = 4
    FORM = 5
    JUPYTER = 6
    DATASET = 7

    KIND_SECTION = (
        (TEXT, 'text'),
        (GALLERY, 'gallery'),
        (FILES, 'files'),
        (USERS, 'profiles'),
        (SLIDERS, 'sliders'),
        (FORM, 'form'),
        (JUPYTER, 'jupyter'),
        (DATASET, 'dataset')
    )

    text = models.TextField(default='', help_text='Текст')
    kind = models.PositiveIntegerField(choices=KIND_SECTION, default=TEXT, help_text='Тип')
    payload = models.JSONField(null=True, help_text='Конструкции')
    position = models.PositiveIntegerField(default=0, help_text='Позиция')

    page = models.ForeignKey(Page, on_delete=models.CASCADE, help_text='Страница, на которой находится секция')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, help_text='Пользователь, создавший секцию')

    class Meta:
        ordering = ('position',)

    resolve_fields = ['page_id', 'user_id']
