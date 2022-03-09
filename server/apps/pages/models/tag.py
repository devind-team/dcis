from django.conf import settings
from django.db import models

from devind_helpers.resolve_model import ResolveModel


class Tag(models.Model, ResolveModel):
    """Тег"""

    name = models.CharField(max_length=256, help_text='Название')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, help_text='Пользователь, создавший тег')

    class Meta:
        ordering = ('-created_at',)

    resolve_fields = ['user_id']
