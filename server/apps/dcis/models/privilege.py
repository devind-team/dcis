from django.db import models
from apps.core.models import User

from .project import Period


class Privilege(models.Model):
    """Модель привилегии.

    Привилегий существует список и пополняются они в зависимости от расширения функционала.
    Кроме этого, существуют еще основные привилегии, которые распространяются на весь сайт.
    """

    name = models.CharField(max_length=250, help_text='Наименование привилегии')
    key = models.CharField(max_length=50, help_text='Ключ привилегии')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')

    class Meta:
        ordering = ('key', 'id',)


class PeriodGroup(models.Model):
    """Модель групп пользователей для периода."""

    name = models.CharField(max_length=250, help_text='Наименование группы периода привилегии')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')

    period = models.ForeignKey(Period, on_delete=models.CASCADE, help_text='Период')
    users = models.ManyToManyField(User, help_text='Пользователи')
    privileges = models.ManyToManyField(Privilege, help_text='Период группы привилегии')

    class Meta:
        ordering = ('name', '-created_at',)


class PeriodPrivilege(models.Model):
    """Модель отдельных привилегий пользователей."""

    period = models.ForeignKey(Period, on_delete=models.CASCADE, help_text='Период')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Пользователь')
    privilege = models.ForeignKey(Privilege, on_delete=models.CASCADE, help_text='Привилегия')

    class Meta:
        unique_together = [['period', 'user', 'privilege']]
