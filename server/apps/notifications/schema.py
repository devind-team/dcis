from typing import Dict, Type

import graphene
from devind_notifications.models import Notice
from devind_notifications.schema.interfaces import NoticeInterface as BaseNotificationInterface
from graphql import ResolveInfo


class NoticeInterface(BaseNotificationInterface):
    """Переопределение стандартного интерфейса уведомлений."""

    @classmethod
    def resolve_type(cls, notice: Notice, info: ResolveInfo):
        """Функция разрешения отдаваемых типов."""
        from devind_notifications.schema.types import NoticeEmptyType, NoticeMailingType
        resolver: Dict[int, Type[graphene.ObjectType]] = {
            notice.INFO: NoticeEmptyType,
            notice.MAILING: NoticeMailingType,
            notice.HAPPY_BIRTHDAY: NoticeEmptyType
        }
        return resolver.get(notice.kind, NoticeEmptyType)
