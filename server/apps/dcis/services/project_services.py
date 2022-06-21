from typing import Sequence
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
    - пользователь добавлен в настройки пользователей
    """
    if user.has_perm('dcis.view_project'):
        return Project.objects.all()
    # 1. Пользователь создал проекты или участвует
    project_users_id: Sequence[int] = Project.objects\
        .filter(Q(user=user) | Q(period__periodgroup__users=user))\
        .values_list('pk', flat=True)
    # 2. Пользователь участвует в дивизионах
    user_divisions: list[dict[str, str | int]] = get_user_divisions(user)
    divisions: dict[str, DivisionModelType] = {
        division_name: [
            user_division['id'] for user_division in user_divisions if user_division['model'] == division_name
        ]
        for division_name in Project.DIVISION_KIND.keys()
    }
    divisions = {dn: dv for dn, dv in divisions.items() if dv}
    project_filter = Q()
    for division_name, division_values in divisions.items():
        project_filter |= Q(content_type__model=division_name, period__division__object_id__in=division_values)
    project_divisions_id: Sequence[int] = Project.objects.filter(project_filter).values_list('pk', flat=True)
    return Project.objects.filter(pk__in=[*project_users_id, *project_divisions_id])

