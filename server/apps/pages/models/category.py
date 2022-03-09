from django.conf import settings
from django.db import models

from devind_helpers.resolve_model import ResolveModel


class Category(models.Model, ResolveModel):
    """Категория"""

    avatar = models.FileField(upload_to='storage/pages/avatars/', default=None, null=True, help_text='Аватар')
    text = models.CharField(max_length=1023, help_text='Текст')
    position = models.PositiveIntegerField(default=0, help_text='Позиция вывода')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, help_text='Родительская категория')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, help_text='Пользователь, создавший категорию')

    class Meta:
        ordering = ('position',)

    resolve_fields = ['user_id', 'parent_id']
