"""Разрешения на работу с проектами сборов."""

from django.core.exceptions import PermissionDenied
from devind_helpers.permissions import ModelPermission

from apps.core.models import User
from apps.dcis.models import Project


def can_view_project(user: User, obj: Project):
    """Пропускает пользователей, которые могут просматривать проект."""
    from apps.dcis.services.project_services import get_user_projects
    if obj in get_user_projects(user):
        return
    raise PermissionDenied('Недостаточно прав для просмотра проекта')


def can_add_project(user: User):
    """Пропускает пользователей, которые могут изменять проект, без проверки возможности просмотра."""
    if user.has_perm('dcis.add_project'):
        return
    raise PermissionDenied('Недостаточно прав для изменения проекта')


def can_change_project_base(user: User, obj: Project):
    """Пропускает пользователей, которые могут изменять проект, без проверки возможности просмотра."""
    if user.has_perm('dcis.change_project') or (
            obj.user_id == user.id and user.has_perm('dcis.add_project')
    ):
        return
    raise PermissionDenied('Недостаточно прав для изменения проекта')


def can_change_project(user: User, obj: Project):
    """Пропускает пользователей, которые могут просматривать и изменять проект."""
    can_view_project(user, obj)
    can_change_project_base(user, obj)


def can_delete_project_base(user: User, obj):
    """Пропускает пользователей, которые могут удалять проект, без проверки возможности просмотра."""
    if user.has_perm('dcis.delete_project') or (
            obj.user_id == user.id and
            user.has_perm('dcis.add_project') and
            obj.period_set.count() == 0
    ):
        return
    raise PermissionDenied('Недостаточно прав для удаления проекта')


def can_delete_project(user: User, obj: Project):
    """Пропускает пользователей, которые могут просматривать и удалять проект."""
    can_view_project(user, obj)
    can_delete_project_base(user, obj)
