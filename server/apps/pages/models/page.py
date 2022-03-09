from django.conf import settings
from django.db import models

from devind_helpers.resolve_model import ResolveModel
from .category import Category
from .page_kind import PageKind
from .tag import Tag


class Page(models.Model, ResolveModel):
    """Страница"""

    title = models.CharField(max_length=1023, help_text='Заголовок')
    avatar = models.FileField(upload_to='storage/pages/', null=True, help_text='Аватар')
    parallax = models.BooleanField(default=False, help_text='Показывать параллакс или нет')
    views = models.PositiveIntegerField(default=0, help_text='Количество просмотров')
    signature = models.CharField(max_length=100, null=True, help_text='Подпись страницы')
    hide = models.BooleanField(default=False, help_text='Скрываем ли страницу')
    priority = models.BooleanField(default=False, help_text='Приоритет')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, help_text='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='Категория')
    kind = models.ForeignKey(PageKind, null=True, on_delete=models.SET_NULL, help_text='Тип')

    tags = models.ManyToManyField(Tag, help_text='Теги на странице')

    class Meta:
        ordering = ('-priority', '-created_at')

    resolve_fields = ['category_id', 'user_id']
