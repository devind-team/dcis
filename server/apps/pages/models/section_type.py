from django.db import models

from apps.core.models import User


class SectionType(models.Model):
    """Тип секции."""

    name = models.CharField(max_length=500, unique=True, help_text='Название типа')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания типа')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления типа')

    author = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, help_text='Автор типа')
