from typing import Optional

from django.db import models

from apps.core.models import User
from .project import Period


class Status(models.Model):
    """Модель статусов документов."""

    name = models.CharField(max_length=250, help_text='Название статуса')
    edit = models.BooleanField(default=False, help_text='Можно ли редактировать документ со статусом')
    protected = models.BooleanField(default=True, help_text='Является ли статус защищенным от изменения')
    comment = models.TextField(null=True, help_text='Комментарий')

    class Meta:
        ordering = ('id',)


class Sheet(models.Model):
    """Модель листа для вывода."""

    name = models.CharField(max_length=250, help_text='Наименование')
    position = models.PositiveIntegerField(default=0, help_text='Позиция')
    comment = models.TextField(max_length=1023, help_text='Комментарий')

    show_head = models.BooleanField(default=True, null=False, help_text='Показывать ли головам')
    show_child = models.BooleanField(default=True, null=False, help_text='Показывать ли подведомственным')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    period = models.ForeignKey(Period, on_delete=models.CASCADE, help_text='Период')

    class Meta:
        ordering = ('position',)
        indexes = [
            models.Index(fields=['period', 'position'])
        ]


class Document(models.Model):
    """Модель документа.

    Когда начинается сбор, берутся атрибуты и листы привязанные к периоду.
    На основе листов и атрибутов создается документ для дивизиона.

    - sheet - список листов в собираемом документе.
    - content_type - Department, Organization - выбирается из проекта.
    - object_id - идентификатор Department, Organization.
        None в случае если для всех дивизионов один сбор.
    """

    comment = models.TextField(max_length=1023, help_text='Комментарий')
    version = models.PositiveIntegerField(default=0, help_text='Версия документа')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, help_text='Пользователь, добавивший документ')
    period = models.ForeignKey(Period, on_delete=models.CASCADE, help_text='Период')
    sheets = models.ManyToManyField(Sheet)

    object_id = models.PositiveIntegerField(null=True, help_text='Идентификатор дивизиона')
    object_name = models.CharField(max_length=512, null=True, help_text='Название дивизиона')

    @property
    def last_status(self) -> Optional['DocumentStatus']:
        try:
            return self.documentstatus_set.latest('created_at')
        except DocumentStatus.DoesNotExist:
            return None

    @property
    def is_editable(self) -> bool:
        last_status = self.last_status
        if last_status is None or not last_status.status.edit:
            return False
        return True

    class Meta:
        ordering = ('-version', '-created_at',)
        unique_together = (('period', 'version', 'object_id',),)


class DocumentStatus(models.Model):
    """Модель статуса документа."""

    comment = models.TextField(max_length=1023, help_text='Комментарий')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')

    document = models.ForeignKey(Document, on_delete=models.CASCADE, help_text='Документ')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, help_text='Статус')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Пользователь')

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['document', 'status']),
            models.Index(fields=['document', 'status', 'user'])
        ]


class Attribute(models.Model):
    """Не табличные данные хранятся в атрибутах.

    Модель содержит список не табличных данных для организации сбора в указанный период.
    Информация о типах:
        - TEXT - тестовое поле
        - MONEY - поле для ввода денег
    """

    TEXT = 'text'
    MONEY = 'money'
    BOOL = 'bool'
    BIG_MONEY = 'bigMoney'
    FILES = 'files'
    NUMERIC = 'numeric'
    DATE = 'date'

    KIND_ATTRIBUTE = (
        (TEXT, 'text'),
        (MONEY, 'money'),
        (BOOL, 'boolean'),
        (BIG_MONEY, 'bigMoney'),
        (FILES, 'files'),
        (NUMERIC, 'numeric'),
        (DATE, 'date')
    )

    name = models.CharField(max_length=100, help_text='Наименование атрибута')
    placeholder = models.CharField(max_length=100, help_text='Подсказка')
    key = models.CharField(max_length=30, help_text='Ключ')
    kind = models.CharField(max_length=10, default=TEXT, choices=KIND_ATTRIBUTE, help_text='Тип атрибута')
    default = models.TextField(help_text='Значение по умолчанию')
    mutable = models.BooleanField(default=True, help_text='Можно ли изменять')

    period = models.ForeignKey(Period, on_delete=models.CASCADE, help_text='Период')
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, help_text='Родительские данные для сбора')

    class Meta:
        ordering = ('key', 'id',)


class AttributeValue(models.Model):
    """Модель значения параметра."""

    value = models.TextField(help_text='Значение')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    document = models.ForeignKey(Document, on_delete=models.CASCADE, help_text='Документ')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, help_text='Атрибут')

    class Meta:
        indexes = [
            models.Index(fields=['document', 'attribute'])
        ]
