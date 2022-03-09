"""Модуль, обеспечивающий хранения перевода."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .language import Language


class Translation(models.Model):
    """Абстрактная модель хранения переводов."""

    object_id = models.PositiveIntegerField(help_text='Идентификатор модели')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, help_text='Переводимая модель')
    content_object = GenericForeignKey('content_type', 'object_id')

    field = models.CharField(max_length=100, help_text='Переводимое поле модели')
    content = models.TextField(help_text='Переведенный контент')

    language = models.ForeignKey(Language, on_delete=models.CASCADE, help_text='Локаль')
