from django.db import models

from apps.pages.decorators import translate_model


@translate_model(['name'])
class PageKind(models.Model):
    """Тип страницы"""

    name = models.CharField(max_length=20, help_text='Название')
