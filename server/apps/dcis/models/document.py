from django.db import models

from apps.core.models import User
from .project import Period


class Status(models.Model):
    """Модель статусов документов."""

    name = models.CharField(max_length=250, help_text='Наименование статуса')
    edit = models.BooleanField(default=False, help_text='Можно ли редактировать')
    comment = models.TextField(null=True, help_text='Комментарий')

    class Meta:
        ordering = ('id',)


class Sheet(models.Model):
    """Модель листа для вывода."""

    name = models.CharField(max_length=250, help_text='Наименование')
    position = models.PositiveIntegerField(default=0, help_text='Позиция')
    comment = models.TextField(max_length=1023, help_text='Комментарий')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    period = models.ForeignKey(Period, on_delete=models.CASCADE, help_text='Период')

    class Meta:
        ordering = ('position',)
        indexes = [
            models.Index(fields=['period', 'position'])
        ]

    def move_merged_cells(self, idx: int, offset: int, delete: bool = False):
        """Двигаем объединенные строки в зависимости от добавления или удаления.

        В будущем метод нужно сделать универсальным (и для колонок).
        """
        for merge_cells in self.mergedcell_set.all():
            if merge_cells.min_row <= idx <= merge_cells.max_row:
                merge_cells.max_row += offset
                if not delete and merge_cells.min_row == idx:
                    merge_cells.min_row += offset
            elif merge_cells.min_row > idx:
                merge_cells.min_row += offset
                merge_cells.max_row += offset
            if merge_cells.min_row > merge_cells.max_row or len(merge_cells.cells) == 1:
                merge_cells.delete()
            else:
                merge_cells.save(update_fields=('min_row', 'max_row',))


class Document(models.Model):
    """Модель документа.

    Когда начинается сбор, берутся атрибуты и листы привязанные к периоду.
    На основе листов и атрибутов создается документ для дивизиона.

    sheet - список листов в собираемом документе.

    content_type - Department, Organization - выбирается из проекта.
    object_id - идентификатор Department, Organization.
        None в случае если для всех дивизионов один сбор.
    """

    comment = models.TextField(max_length=1023, help_text='Комментарий')
    version = models.PositiveIntegerField(default=0, help_text='Версия документа')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    period = models.ForeignKey(Period, on_delete=models.CASCADE, help_text='Период')
    sheets = models.ManyToManyField(Sheet)

    object_id = models.PositiveIntegerField(null=True, help_text='Идентификатор дивизиона')

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

    TEXT = 0
    MONEY = 1

    KIND_ATTRIBUTE = (
        (TEXT, 'text'),
        (MONEY, 'money'),
    )

    name = models.CharField(max_length=100, help_text='Наименование атрибута')
    placeholder = models.CharField(max_length=100, help_text='Подсказка')
    key = models.CharField(max_length=30, help_text='Ключ')
    kind = models.PositiveIntegerField(default=TEXT, choices=KIND_ATTRIBUTE, help_text='Тип атрибута')
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
