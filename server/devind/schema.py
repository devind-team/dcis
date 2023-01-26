import devind_core.schema
import devind_dictionaries.schema
import devind_notifications.schema
import graphene
from graphene_django.debug import DjangoDebug

import apps.core.schema
import apps.dashboard.schema
import apps.dcis.schema
import apps.notifications.schema


class Query(
    devind_core.schema.Query,
    devind_notifications.schema.Query,
    apps.dashboard.schema.Query,
    apps.dcis.schema.Query,
    devind_dictionaries.schema.Query,
    graphene.ObjectType
):
    """Схема запросов данных."""

    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(
    devind_core.schema.Mutation,
    devind_notifications.schema.Mutation,
    apps.core.schema.Mutation,
    apps.dcis.schema.Mutation,
    graphene.ObjectType
):
    """Мутации на изменение чего-либо."""

    pass


class Subscription(
    devind_notifications.schema.Subscription,
    graphene.ObjectType
):
    """Подписки на сокеты."""

    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    types=(*devind_notifications.schema.types,)
)
