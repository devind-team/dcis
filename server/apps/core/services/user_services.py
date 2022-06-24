from typing import Union, Optional, Type
from graphql_relay import from_global_id
from devind_helpers.orm_utils import get_object_or_none
from apps.core.models import User
from graphql import ResolveInfo


def relation_division(user: User, data: dict[str, Union[str, int]]) -> None:
    """Привязка авторизуемого пользователя к дивизиону."""
    from devind_dictionaries.models import Organization, Department
    from apps.dcis.models import Project

    division_type: Optional[str] = data.get('id_vid_uchr')
    relation: dict[str, str] = {
        '1': 'organization',
        # '2': 'department',
    }
    org_id: Optional[int] = data.get('IdListEdu')
    if division_type not in relation or org_id is None:
        return
    DivisionModel: Type[Union[Department, Organization]] = Project.DIVISION_KIND[relation[division_type]]  # noqa
    division = get_object_or_none(DivisionModel, pk=org_id)
    if division is None:
        return
    getattr(user, f'{relation[division_type]}s').add(division)


def get_user_from_id_or_context(info: ResolveInfo, user_id: str | int | None = None) -> User:
    """Получаем пользователя"""
    if user_id is None:
        return info.context.user
    if type(user_id) == str:
        user_id = from_global_id(user_id)[1]
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return info.context.user
