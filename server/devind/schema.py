import graphene
import devind_core.schema
import devind_notifications.schema
import devind_dictionaries.schema
import apps.core.schema
import apps.dashboard.schema
import apps.dcis.schema
import apps.pages.schema
import apps.notifications.schema
from graphene_django.debug import DjangoDebug


class Query(
    devind_core.schema.Query,
    devind_notifications.schema.Query,
    apps.dashboard.schema.Query,
    apps.dcis.schema.Query,
    apps.pages.schema.Query,
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
    apps.pages.schema.Mutation,
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
    types=(*apps.pages.schema.types, *devind_notifications.schema.types, *apps.notifications.schema.types)
)
