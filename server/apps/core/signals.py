"""Описание сигналов для записи изменений в моделях."""
from .models import User
from auditlog.registry import auditlog
from devind_core.models import File
from django.contrib.auth.models import Group


auditlog.register(User)
auditlog.register(File)
auditlog.register(Group)
