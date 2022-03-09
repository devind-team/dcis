from django.conf import settings
from django.db import models

from .page import Page


class Comment(models.Model):
    """Комментарий"""

    text = models.CharField(max_length=1023, help_text='Текст')
    rating = models.IntegerField(default=0, help_text='Рейтинг')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text='Пользователь, оставивший комментарий')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, help_text='Страница, на которой был оставлен комментарий')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        help_text='Родительский комментарий в дереве'
    )
