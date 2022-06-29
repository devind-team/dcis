"""Разрешения на работу с проектами сборов."""
from devind_helpers.permissions import BasePermission, ModelPermission

from apps.dcis.models import Project
from apps.dcis.services.project_services import get_user_projects


class ViewProject(BasePermission):
    """Пропускает пользователей, которые могут просматривать проект."""

    @staticmethod
    def has_object_permission(context, obj: Project):
        return obj in get_user_projects(context.user)


AddProject = ModelPermission('dcis.add_project')


class ChangeProject(BasePermission):
    """Пропускает пользователей, которые могут изменять проект."""

    @staticmethod
    def has_object_permission(context, obj: Project):
        return all((
            ViewProject.has_object_permission(context, obj),
            context.user.has_perm('dcis.change_project') or all((
                obj.user_id == context.user.id,
                context.user.has_perm('dcis.add_project'),
            )),
        ))


class DeleteProject(BasePermission):
    """Пропускает пользователей, которые могут удалять проект."""

    @staticmethod
    def has_object_permission(context, obj: Project):
        return all((
            ViewProject.has_object_permission(context, obj),
            context.user.has_perm('dcis.delete_project') or all((
                obj.user_id == context.user.id,
                context.user.has_perm('dcis.add_project'),
                obj.period_set.count() == 0,
            )),
        ))
