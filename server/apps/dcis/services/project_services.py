from typing import Sequence

from django.db.models import QuerySet, Q
from apps.core.models import User
from apps.dcis.models import Project
from apps.dcis.helpers.divisions import get_user_division_ids


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
    divisions: dict[str, str | int] = get_user_division_ids(user)
    project_filter = Q()
    for division_name, division_values in divisions.items():
        project_filter |= Q(content_type__model=division_name, period__division__object_id__in=division_values)
    project_divisions_id: Sequence[int] = Project.objects.filter(project_filter).values_list('pk', flat=True)
    return Project.objects.filter(pk__in=[*project_users_id, *project_divisions_id])

