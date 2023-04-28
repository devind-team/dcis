import os
import uuid

from django.db import models
from model_clone import CloneMixin

from apps.core.models import User
from .project import Period


def file_directory_path(instance: 'DocumentScan', filename: str) -> str:
    """Формируем автоматический путь директории методических рекомендаций."""
    uuid_name = str(instance.id)[:2].lower()
    return f'storage/documents_scans/{uuid_name}/{instance.id}{os.path.splitext(filename)[1]}'


class Status(models.Model):
    """Модель статусов документов."""

    name = models.CharField(max_length=250, help_text='Название статуса')
    edit = models.BooleanField(default=False, help_text='Можно ли редактировать документ со статусом')
    comment = models.TextField(null=True, help_text='Комментарий')

    class Meta:
        ordering = ('id',)


class AddStatus(models.Model):
    """Модель, определяющая сценарии добавления статусов."""

    from_status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        null=True,
        related_name='from_add_statuses',
        help_text='Изначальный статус'
    )
    to_status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='to_add_statuses',
        help_text='Новый статус'
    )
    roles = models.JSONField(help_text='Роли пользователей, которые могут изменять статус')
    action = models.CharField(max_length=250, help_text='Действие при добавлении статуса в документ')


class Sheet(models.Model, CloneMixin):
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


class Document(models.Model, CloneMixin):
    """Модель документа.

    Когда начинается сбор, берутся атрибуты и листы привязанные к периоду.
    На основе листов и атрибутов создается документ для дивизиона.

    - sheet - список листов в собираемом документе.
    - content_type - Department, Organization - выбирается из проекта.
    - object_id - идентификатор Department, Organization.
        None в случае если для всех дивизионов один сбор.
    """

    version = models.PositiveIntegerField(default=0, help_text='Версия документа')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    updated_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='updated_by_document_set',
        help_text='Пользователь, обновивший документ'
    )
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='document_set',
        help_text='Пользователь, добавивший документ'
    )
    period = models.ForeignKey(Period, on_delete=models.CASCADE, help_text='Период')
    sheets = models.ManyToManyField(Sheet, help_text='Листы документа')

    object_id = models.PositiveIntegerField(null=True, help_text='Идентификатор дивизиона')
    object_name = models.CharField(max_length=512, null=True, help_text='Название дивизиона')

    last_status = models.ForeignKey(
        'DocumentStatus',
        null=True,
        on_delete=models.SET_NULL,
        related_name='last_status_document_set',
        help_text='Последний статус документа',
    )
    scan: 'DocumentScan'

    @property
    def is_editable(self) -> bool:
        if self.last_status is None or not self.last_status.status.edit:
            return False
        return True

    class Meta:
        ordering = ('-version', '-created_at',)
        unique_together = (('period', 'version', 'object_id',),)


class DocumentStatusManager(models.Manager):
    """Менеджер модели статуса документа для управления последним статусом документа."""

    def create(self, *args, **kwargs) -> 'DocumentStatus':
        """Создание статуса документа."""
        document_status = super().create(*args, **kwargs)
        document_status.document.last_status = document_status
        document_status.document.save(update_fields=('last_status',))
        return document_status


class DocumentStatus(models.Model, CloneMixin):
    """Модель статуса документа."""

    comment = models.TextField(max_length=1023, help_text='Комментарий')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')

    document = models.ForeignKey(Document, on_delete=models.CASCADE, help_text='Документ')
    archive_period = models.ForeignKey(Period, null=True, on_delete=models.CASCADE, help_text='Архивированный период')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, help_text='Статус')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Пользователь')

    objects = DocumentStatusManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        super().save(force_insert, force_update, using, update_fields)
        if update_fields and 'created_at' in update_fields:
            self.document.last_status = self.document.documentstatus_set.latest('created_at')
            self.document.save(update_fields=('last_status',))

    def delete(self, *args, **kwargs):
        """Удаление статуса документа."""
        is_last = self == self.document.last_status
        result = super().delete(*args, **kwargs)
        if is_last:
            try:
                self.document.last_status = self.document.documentstatus_set.latest('created_at')
            except DocumentStatus.DoesNotExist:
                self.document.last_status = None
            self.document.save(update_fields=('last_status',))
        return result

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['document', 'status']),
            models.Index(fields=['document', 'status', 'user'])
        ]


class Attribute(models.Model, CloneMixin):
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
    default = models.TextField(null=True, help_text='Значение по умолчанию')
    mutable = models.BooleanField(default=True, help_text='Можно ли изменять')
    position = models.PositiveIntegerField(default=0, help_text='Позиция в выводе')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    period = models.ForeignKey(Period, on_delete=models.CASCADE, help_text='Период')
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, help_text='Родительские данные для сбора')

    class Meta:
        ordering = ('created_at',)
        unique_together = (('key', 'period',),)


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


class Limitation(models.Model):
    """Ограничения, накладываемые на лист."""

    index = models.PositiveSmallIntegerField(help_text='Индекс, начиная с 1, для вывода и расчета')
    formula = models.TextField(help_text='Формула')
    error_message = models.TextField(help_text='Сообщение об ошибке')

    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, help_text='Лист')

    class Meta:
        ordering = ('index',)


class DocumentScan(models.Model):
    """Модель скана документа"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, help_text='Название файла')
    src = models.FileField(upload_to=file_directory_path, help_text='Путь к файлу')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата добавления файла')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления файла')

    document = models.OneToOneField(
        Document,
        null=True,
        primary_key=False,
        related_name='scan',
        on_delete=models.CASCADE,
        help_text='Скан документа'
    )
