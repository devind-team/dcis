"""Описание сигналов для записи изменений в моделях."""
from auditlog.registry import auditlog
from django.contrib.auth.models import Group
from devind_core.models import File
from .models import User


auditlog.register(User)
auditlog.register(File)
auditlog.register(Group)
