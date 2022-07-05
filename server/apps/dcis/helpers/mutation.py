import graphene
from devind_helpers.schema.types import ErrorFieldType
from graphene_django_cud.mutations.core import DjangoCudBase


class DjangoCudBaseMutation(DjangoCudBase):
    """Базовая мутация."""

    class Meta:
        abstract = True

    success = graphene.Boolean(required=True, description='Успех мутации')
    errors = graphene.List(graphene.NonNull(ErrorFieldType), required=True, description='Ошибки мутации')

    def __init__(self, *args, **kwargs):
        super(DjangoCudBaseMutation, self).__init__(*args, **kwargs)
        if self.success is None:
            self.success = True
        if self.errors is None:
            self.errors = []

    def add_error(self, field: str, messages: list[str]) -> None:
        """Добавление ошибки.

        :param field: поле ошибки
        :param messages: сообщения ошибки
        """
        self.errors.append(ErrorFieldType(field=field, messages=messages))
