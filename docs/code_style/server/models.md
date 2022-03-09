# Оформление моделей

1. Файловая структура.  

1.1. Модели должны располагаться в папке models каждого приложения.  
1.2. Файлы моделей должны быть названы в единственном числе.  
1.3. Разделение моделей на файлы может быть произвольным.

2. Оформление модели.  

2.1. Модель должна называться в единственном числе и содержать документирование.
```python
from django.db import models

class Page(models.Model):
    """Страница
    
    Длинное описание.
    """

    ...

class User(models.Model):
    """Пользователь"""

    ...
```
2.2. Каждое поле модели должно содержать описание с помощью параметра help_text.
```python

from django.db import models

class User(models.Model):
    """Пользователь"""

    name = models.CharField(max_length=128, help_text='Имя')
```
2.3. Модель не должна содержать методов с бизнес-логикой.
Допустимы свойства, зависящие исключительно от полей модели и других свойств.  
2.4. Порядок полей следующий:
```python
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.core.helpers.resolve_model import ResolveModel

class Model(models, ResolveModel):
    """Модель"""
    
    # 1. Enums
    FIELD1 = 1
    FIELD2 = 2
    FIELDS = (
        (FIELD1, 'field1'),
        (FIELD2, 'field2')
    )

    # 2. Generic relations
    object_id = models.PositiveIntegerField(help_text='Идентификатор модели')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, help_text='Модель')
    content_object = GenericForeignKey('content_type', 'object_id')

    # 3. Scalar fields
    text = models.TextField(help_text='Текст')
    boolean = models.BooleanField(help_text='Флаг')
    kind = models.PositiveIntegerField(choices=FIELDS, default=FIELD1, help_text='Тип')

    # 4. created_at, updated_at
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')

    # 5. OneToOne fields
    one_to_one = models.OneToOneField(
        'ExternalModel1',
        on_delete=models.CASCADE,
        primary_key=True,
        help_text='Один к одному'
    )

    # 6. ForeignKey fields
    foreign_key = models.ForeignKey(
        'ExternalModel2',
        on_delete=models.CASCADE,
        help_text='Внешний ключ'
    )

    # 7. ManyToMany fields
    many_to_many = models.ManyToManyField(
        'ExternalModel3',
        help_text='Многие ко многим'
    )
    
    # 8. Meta
    class Meta:
        ordering = ('created_at', 'id',)

    # 9. Resolve fields
    resolve_fields = ['foreign_key_id']

    # 10. Managers
    class _ObjectsManager(models.Manager):
        ...
        
    objects = _ObjectsManager()

    # 11. Rest fields
    @property
    def property_field(self):
        ...
```