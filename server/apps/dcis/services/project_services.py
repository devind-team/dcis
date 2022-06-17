from typing import Union
from django.db.models import QuerySet, Q
from apps.core.models import User
from apps.dcis.models import Project

from .divisions_services import get_user_divisions
from ..schema.types import DivisionModelType


def get_projects(user: User) -> QuerySet:
    """Получение проектов пользователя.

    Пользователь видит проект:
    - привилегия dcis.view_project - получаются все привилегии
    - пользователь создал этот проект
    - пользователь участвует в проекте
    """
    if user.has_perm('dcis.view_project'):
        return Project.objects.all()
    project_filter = Q(user=user)
    user_divisions: list[dict[str, Union[str, int]]] = get_user_divisions(user)
    divisions: dict[str, DivisionModelType] = {
        division_name: [
            user_division['id'] for user_division in user_divisions if user_division['model'] == division_name
        ]
        for division_name in Project.DIVISION_KIND.keys()
    }
    divisions = {dn: dv for dn, dv in divisions.items() if dv}
    for division_name, division_values in divisions.items():
        project_filter |= Q(content_type__model=division_name, period__division__object_id__in=division_values)
    return Project.objects.filter(project_filter)

