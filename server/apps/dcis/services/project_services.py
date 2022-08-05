"""Модуль, отвечающий за работу с проектами."""

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, QuerySet

from apps.core.models import User
from apps.dcis.models import Project
from apps.dcis.permissions import can_add_project, can_change_project, can_delete_project
from apps.dcis.services.divisions_services import get_user_division_ids


def get_user_participant_projects(user: User) -> QuerySet[Project]:
    """Получение проектов, в которых пользователь непосредственно участвует."""
    return Project.objects.filter(Q(user=user) | Q(period__user=user) | Q(period__periodgroup__users=user))


def get_user_privileges_projects(user: User) -> QuerySet[Project]:
    """Получение проектов, связанных с привилегиями пользователя."""
    return Project.objects.filter(period__periodprivilege__user=user)


def get_user_divisions_projects(user: User) -> QuerySet[Project]:
    """Получение проектов, связанных с дивизионами пользователя."""
    projects = Project.objects.none()
    divisions = get_user_division_ids(user)
    for division_name, division_values in divisions.items():
        projects |= Project.objects.filter(
            content_type__model=division_name,
            period__division__object_id__in=division_values
        )
    return projects


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


def create_project(user: User, validate_field: dict, visibility: bool) -> Project:
    """Создание периода."""
    can_add_project(user)
    return Project.objects.create(
            name=validate_field['name'],
            short=validate_field['short'],
            description=validate_field['description'],
            content_type=ContentType.objects.get_for_model(Project.DIVISION_KIND.
                                                           get(validate_field['content_type'], Department)),
            visibility=visibility)


def change_project(
        user: User,
        project: Project,
        name: str,
        short: str,
        description: str,
        visibility: bool,
        archive: bool) -> Project:
    """Изменение настроек проекта."""
    can_change_project(user, project)
    project.name = name
    project.short = short
    project.description = description
    project.visibility = visibility
    project.archive = archive
    project.save(update_fields=('name', 'short', 'description', 'visibility', 'archive', 'updated_at'))
    return project


def delete_project(user: User, project: Project) -> None:
    """Удаление проекта."""
    can_delete_project(user, project)
    project.delete()
