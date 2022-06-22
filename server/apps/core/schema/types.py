from typing import Set

import graphene
from django.db.models import QuerySet
from graphene.relay import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django_optimizer import resolver_hints
from graphql import ResolveInfo

from apps.core.models import User
from devind_core.filters import UserFilterSet
from devind_core.schema.connections.countable_connection import CountableConnection
from devind_helpers.optimized import OptimizedDjangoObjectType
from apps.dcis.services.divisions_services import get_user_divisions


class UserType(OptimizedDjangoObjectType):
    """Описание пользовательского типа."""

    session = graphene.Field('devind_core.schema.types.SessionType', description='Сессия пользователя')
    groups = graphene.List('devind_core.schema.types.GroupType', required=True, description='Группы пользователя')
    permissions = graphene.List(graphene.String, required=True, description='Привилегии пользователя')
    notices = DjangoFilterConnectionField('devind_notifications.schema.NoticeType')
    notifications = DjangoFilterConnectionField('devind_notifications.schema.NotificationType')
    profile_values = graphene.List('devind_core.schema.types.ProfileValueType')
    divisions = graphene.List('apps.dcis.schema.types.DivisionModelType')

    class Meta:
        model = User
        interfaces = (Node,)
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'sir_name',
            'is_active',
            'avatar',
            'birthday',
            'agreement',
            'created_at',
            'notices',
            'notifications',
            'profile_values',
        )
        filterset_class = UserFilterSet
        connection_class = CountableConnection

    @staticmethod
    def resolve_session(user: User, info: ResolveInfo) -> QuerySet:
        from devind_core.models import Session
        token: str | None = info.context.META.get('HTTP_AUTHORIZATION', None)
        return user.session_set.latest('created_at') \
            if token is None \
            else Session.objects.get(access_token__token=token[7:])

    @staticmethod
    @resolver_hints(model_field='groups')
    def resolve_groups(user: User, info: ResolveInfo) -> QuerySet:
        return user.groups.all()

    @staticmethod
    @resolver_hints(model_field='user_permissions')
    def resolve_permissions(user: User, info: ResolveInfo) -> Set[str]:
        return user.get_all_permissions()

    @staticmethod
    @resolver_hints(model_field='notice_set')
    def resolve_notices(user: User, info: ResolveInfo) -> QuerySet:
        return user.notice_set.all()

    @staticmethod
    @resolver_hints(model_field='notification_set')
    def resolve_notifications(user: User, info: ResolveInfo) -> QuerySet:
        return user.notification_set.all()

    @staticmethod
    @resolver_hints(model_field='profilevalue_set')
    def resolve_profile_values(user: User, info: ResolveInfo) -> QuerySet['apps.core.schema.types.ProfileValueType']:
        return user.profilevalue_set.all()

    @staticmethod
    def resolve_divisions(user: User, info: ResolveInfo):
        return get_user_divisions(user)
