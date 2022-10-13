from devind_dictionaries.models import Organization
from django.db import models

from apps.core.models import User


class CuratorGroup(models.Model):
    """Модель группы кураторов."""

    name = models.CharField(max_length=250, help_text='Наименование кураторской группы')

    users = models.ManyToManyField(User, help_text='Пользователь кураторской группы')
    organization = models.ManyToManyField(Organization, help_text='Организация кураторской группы')

    class Meta:
        """Мета класс модели групп кураторов."""
        ordering = ('id',)
