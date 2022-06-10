from typing import cast, Dict, Type, Union
from django.contrib.contenttypes.models import ContentType
from django.db import models
from apps.core.models import User

from devind_core.models import File
from devind_dictionaries.models import Department, Organization


def default_content_type(instance):
    return ContentType.objects.get_by_natural_key('devind_dictionaries', 'department').id


class Project(models.Model):
    """Проект сборов."""

    DIVISION_KIND: Dict[str, Type[Union[Department, Organization]]] = {
        'department': Department,
        'organization': Organization
    }

    name = models.CharField(max_length=250, help_text='Наименование проекта')
    short = models.CharField(max_length=30, help_text='Сокращенное наименование проекта')
    description = models.TextField(max_length=1023, help_text='Описание проекта')
    visibility = models.BooleanField(default=True, help_text='Видимость проекта')
    archive = models.BooleanField(default=False, help_text='Архив')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, help_text='Организатор сборов')
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        default=default_content_type,
        help_text='Тип дивизиона'
    )

    class Meta:
        """Мета класс описания параметров проекта сборов."""
        ordering = ('-created_at',)

    @property
    def division(self) -> Type[Union[Department, Organization]]:
        return self.DIVISION_KIND.get(cast(str, self.content_type.model), Department)


class Period(models.Model):
    """Модель периода проекта.

    - multiple - множественное заполнение, в случае если False, предоставляется один документ на все дивизионы.
    - privately - приватность отвечает за видимость добавленных строк,
        предоставляется ли доступ ко всем строкам или только к тем, которые добавил я.
        Это определяет условие выгрузки строк:
            - все строки - у меня есть права или privately = False
            - только строки пользователя - нет прав и privately = True
    """

    PREPARATION = 'preparation'
    OPEN = 'open'
    CLOSE = 'close'

    KIND_PERIOD = (
        (PREPARATION, 'preparation'),
        (OPEN, 'open'),
        (CLOSE, 'close')
    )

    name = models.CharField(max_length=250, help_text='Наименование периода')
    status = models.CharField(max_length=16, choices=KIND_PERIOD, default=PREPARATION, help_text='Статус проекта')
    multiple = models.BooleanField(default=False, help_text='Множественное заполнение')
    privately = models.BooleanField(default=False, help_text='Приватность полей')

    start = models.DateField(null=True, help_text='Дата начала')
    expiration = models.DateField(null=True, help_text='Дата окончания')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text='Организатор сборов')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text='Проект сборов')
    methodical_support = models.ManyToManyField(File, help_text='Методическая поддержка')

    class Meta:
        """Мета класс с описанием параметров периода."""
        ordering = ('-created_at',)


class Division(models.Model):
    """Участвующие в сборах подразделения.

    Реализация будет осуществляться для двух дивизионов:
        - Department - департамент
        - Organization - организации

    Связь к дивизионам или департамента обеспечивается через content_object
    """

    period = models.ForeignKey(Period, on_delete=models.CASCADE, help_text='Период')
    object_id = models.PositiveIntegerField(help_text='Идентификатор дивизиона')

    class Meta:
        unique_together = [['period', 'object_id']]
