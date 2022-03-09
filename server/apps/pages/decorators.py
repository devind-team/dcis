from typing import Iterable, Callable, Type

import graphene
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from graphql import ResolveInfo

from .models import Translation, Language


def translate_model(fields: Iterable[str]) -> Callable[[Type[models.Model]], Type[models.Model]]:
    """Перевод модели.

    :param fields: поля модели
    """
    def decorator(cls: Type[models.Model]) -> Type[models.Model]:
        cls.add_to_class(
            'translations',
            GenericRelation(
                Translation,
                related_query_name=cls.__name__.lower()
            )
        )
        for field in fields:
            @property
            def translated_field(self):
                translations = self.translations.filter(
                    field=field,
                    language=Language.current_language()
                )
                if translations.count() != 1:
                    return getattr(self, field)
                return translations.first().content
            cls.add_to_class(f'translated_{field}', translated_field)
        return cls
    return decorator


def translate_type(fields: Iterable[str]) -> Callable[[Type[graphene.ObjectType]], Type[graphene.ObjectType]]:
    """Перевод типа.

    :param fields: поля типа
    """

    def decorator(cls: Type[graphene.ObjectType]) -> Type[graphene.ObjectType]:
        for field in fields:
            def resolve(model, info: ResolveInfo):
                return getattr(model, f'translated_{field}')
            setattr(cls, f'resolve_{field}', resolve)
        return cls
    return decorator
