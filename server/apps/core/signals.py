"""Описание сигналов для записи изменений в моделях."""

from django.contrib.auth.models import Group
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from devind_core.models import File, LogEntry
from .models import User


@receiver([post_save, post_delete], sender=User)
def handle_user(sender, instance: User, **kwargs):
    """Логгирование изменения пользователя."""
    LogEntry.logging(sender, instance, **kwargs)


@receiver([post_save, post_delete], sender=File)
def handler_file(sender, instance, **kwargs):
    """Логгирование изменение файла."""
    LogEntry.logging(sender, instance, **kwargs)


@receiver([post_save, post_delete], sender=Group)
def handle_group(sender, instance: Group, **kwargs):
    """Логгирование изменения групп пользователей."""
    LogEntry.logging(sender, instance, **kwargs)
