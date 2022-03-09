from typing import Dict, Type

import graphene
from graphql import ResolveInfo

from apps.pages.models import Page
from apps.pages.schema.types import PageType
from devind_helpers.optimized import OptimizedDjangoObjectType
from devind_helpers.orm_utils import get_object_or_none
from devind_notifications.models import Notice
from devind_notifications.schema.interfaces import NoticeInterface as BaseNotificationInterface


class NoticeInterface(BaseNotificationInterface):
    """Переопределение стандартного интерфейса уведомлений."""

    @classmethod
    def resolve_type(cls, notice: Notice, info: ResolveInfo):
        """Функция разрешения отдаваемых типов."""
        from devind_notifications.schema.types import NoticeEmptyType, NoticeMailingType
        resolver: Dict[int, Type[graphene.ObjectType]] = {
            notice.INFO: NoticeEmptyType,
            notice.MAILING: NoticeMailingType,
            notice.PAGE: NoticePageType,
            notice.HAPPY_BIRTHDAY: NoticeEmptyType
        }
        return resolver.get(notice.kind, NoticeEmptyType)


class NoticePageType(OptimizedDjangoObjectType):
    """Уведомление типа 'Добавлена новая страница'"""

    page = graphene.Field(PageType, description='Страница')

    class Meta:
        model = Notice
        interfaces = (NoticeInterface,)
        fields = ('id', 'kind', 'payload', 'object_id', 'created_at', 'user', 'page',)

    @staticmethod
    def resolve_page(notice: Notice, info: ResolveInfo, *args, **kwargs):
        return get_object_or_none(Page, pk=notice.object_id)


types = [NoticePageType]
