"""Модель списка доступных языков."""

from django.db import models
from django.utils.translation import get_language


class Language(models.Model):
    """Модель, содержащая список доступных языков."""

    name = models.CharField(max_length=100, help_text='Название языка')
    code = models.CharField(max_length=25, help_text='Код языка')

    @classmethod
    def current_language(cls):
        """Получение текущего языка."""
        for language_code in get_language().split(','):
            try:
                return cls.objects.get(code=language_code)
            except cls.DoesNotExist:
                pass
            return cls.objects.get(code='ru')
