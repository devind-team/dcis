"""Модуль сортировок."""

from django.db.models import CharField, QuerySet
from django.db.models.functions import Concat

from apps.dcis.helpers.ordering import OrderedDjangoFilterConnectionField
from apps.dcis.models import Document


class DocumentOrderedDjangoFilterConnectionField(OrderedDjangoFilterConnectionField):
    """Класс, добавляющий аннотации для сортировки документов."""

    @classmethod
    def resolve_queryset(cls, connection, iterable, info, args, filtering_args, filterset_class):
        order: list[str] | None = args.get('orderBy', None)
        if order:
            for key in ('lastStatus', '-lastStatus'):
                try:
                    index = order.index(key)
                    order[index] = order[index].replace('lastStatus', 'combinedLastStatus')
                except ValueError:
                    pass
        return super().resolve_queryset(connection, iterable, info, args, filtering_args, filterset_class)

    @classmethod
    def annotate(cls, qs: QuerySet[Document]) -> QuerySet[Document]:
        """Добавление аннотаций."""
        return qs.annotate(
            division=Concat(
                'object_name', 'object_id',
                output_field=CharField()
            ),
            combined_last_status=Concat(
                'last_status__status__name', 'last_status__created_at', 'last_status__comment',
                output_field=CharField()
            )
        )
