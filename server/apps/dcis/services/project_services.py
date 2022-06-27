"""Модуль, отвечающий за работу с проектами."""

from django.db.models import Q, QuerySet

from apps.core.models import User
from apps.dcis.models import Project
from apps.dcis.services.divisions_services import get_user_division_ids


def get_user_participant_projects(user: User) -> QuerySet[Project]:
    """Получение проектов, в которых пользователь непосредственно участвует."""
    return Project.objects.filter(Q(user=user) | Q(period__user=user) | Q(period__periodgroup__users=user))


def get_user_divisions_projects(user: User) -> QuerySet[Project]:
    """Получение проектов, связанных с дивизионами пользователя."""
    project_filter = Q()
    divisions = get_user_division_ids(user)
    for division_name, division_values in divisions.items():
        project_filter |= Q(content_type__model=division_name, period__division__object_id__in=division_values)
    return Project.objects.filter(project_filter)


def get_user_privileges_projects(user: User) -> QuerySet[Project]:
    """Получение проектов, связанных с привилегиями пользователя."""
    return Project.objects.filter(period__periodprivilege__user=user)


def get_user_projects(user: User) -> QuerySet[Project]:
    """Получение проектов пользователя.

    Пользователь видит проект:
      - пользователь обладает глобальной привилегией dcis.view_project
      - пользователь участвует в проекте
        (создал проект, или создал один из периодов проекта, или состоит в группе одного из периодов проекта)
      - пользователь имеет привилегию для одного из периодов проекта
      - пользователь состоит в дивизионе, который участвует в проекте
    """
    if user.has_perm('dcis.view_project'):
        return Project.objects.all()
    return get_user_participant_projects(user) | get_user_privileges_projects(user) | get_user_divisions_projects(user)
