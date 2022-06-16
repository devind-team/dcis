from typing import Union, Optional, Type
from devind_helpers.orm_utils import get_object_or_none
from apps.core.models import User


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