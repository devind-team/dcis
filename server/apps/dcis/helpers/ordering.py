"""Модуль сортировок."""

import graphene
from django.db.models import QuerySet
from graphene.utils.str_converters import to_snake_case
from graphene_django.filter import DjangoFilterConnectionField


class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):
    """Класс, добавляющий сортировку с помощью `order_by`."""

    @property
    def args(self):
        args = super().args
        args['orderBy'] = graphene.Argument(
            graphene.List(graphene.NonNull(graphene.String)),
            description='Сортировка с помощью `order_by`'
        )
        return args

    @args.setter
    def args(self, args):
        self._base_args = args

    @classmethod
    def resolve_queryset(cls, connection, iterable, info, args, filtering_args, filterset_class):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        qs = cls.annotate(qs)
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        order: list[str] | None = args.get('orderBy', None)
        if order:
            snake_order = [to_snake_case(o) for o in order]
            qs = qs.order_by(*snake_order)
        return qs

    @classmethod
    def annotate(cls, qs: QuerySet) -> QuerySet:
        """Добавление аннотаций."""
        return qs
