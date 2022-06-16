import datetime

from django.utils.timezone import make_aware

from django.conf import settings
from django_cbias_auth.schema import CbiasAuthMutation
from graphql import ResolveInfo
from devind_core.models import Profile, ProfileValue, Session
from devind_helpers.orm_utils import get_object_or_none
from oauth2_provider.models import AccessToken

from apps.core.models import User
from apps.core.services.user_services import relation_division
from .types import UserType


class AuthCbiasMutation(CbiasAuthMutation):
    """Мутация для авторизации пользователя через портал https://cbias.ru."""

    class Meta:
        """Метакласс с параметрами для авторизации"""

        user_type = UserType
        url = settings.EXTERNAL_URLS.get('cbias')
        description = 'Авторизация через портал https://cbias.ru'

    @staticmethod
    def get_user(info: ResolveInfo, payload: dict, data: dict) -> User:
        """Получение пользователя по данным."""
        user = get_object_or_none(User, profilevalue__profile__code='uuid', profilevalue__value=payload.get('uid'))
        if user is None:
            user = User.objects.create(
                username=data['login'],
                last_name=data['Sirname'],
                first_name=data['Name'],
                sir_name=data['PostName'],
                email=data['Email']
            )
            ProfileValue.objects.create(
                profile=Profile.objects.get(code='uuid'),
                user=user,
                value=data['uid']
            )
        user.agreement = make_aware(datetime.datetime.now())
        user.save(update_fields=('agreement',))
        relation_division(user, data)
        return user

    @staticmethod
    def callback(info: ResolveInfo, access_token: AccessToken) -> None:
        ip: str = info.context.META.get('REMOTE_ADDR')
        user_agent: str = info.context.META.get('HTTP_USER_AGENT')
        Session.objects.create(
            ip=ip,
            user_agent=user_agent,
            access_token=access_token,
            user=access_token.user
        )
