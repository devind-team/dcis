"""Разрешения на работу с проектами сборов."""

from django.core.exceptions import PermissionDenied
from devind_helpers.permissions import ModelPermission

from apps.dcis.models import Project
from apps.dcis.services.project_services import get_user_projects


def can_view_project(context, obj: Project):
    """Пропускает пользователей, которые могут просматривать проект."""
    if obj in get_user_projects(context.user):
        return
    raise PermissionDenied('Недостаточно прав для просмотра проекта')


# class ViewProject(BasePermission):
#     """Пропускает пользователей, которые могут просматривать проект."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Project):
#         return obj in get_user_projects(context.user)


AddProject = ModelPermission('dcis.add_project')


def can_change_project_base(context, obj: Project):
    """Пропускает пользователей, которые могут изменять проект, без проверки возможности просмотра."""
    if context.user.has_perm('dcis.change_project') or (
            obj.user_id == context.user.id and context.user.has_perm('dcis.add_project')
    ):
        return
    raise PermissionDenied('Недостаточно прав для изменения проекта')


# class ChangeProjectBase(BasePermission):
#     """Пропускает пользователей, которые могут изменять проект, без проверки возможности просмотра."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Project):
#         return context.user.has_perm('dcis.change_project') or (
#                 obj.user_id == context.user.id and context.user.has_perm('dcis.add_project')
#         )

def can_change_project(context, obj: Project):
    """Пропускает пользователей, которые могут просматривать и изменять проект."""
    can_view_project(context, obj)
    can_change_project_base(context, obj)


# class ChangeProject(BasePermission):
#     """Пропускает пользователей, которые могут просматривать и изменять проект."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Project):
#         can_view_project(context, obj)
#         can_change_project_base(context, obj)


def can_delete_project_base(context, obj):
    """Пропускает пользователей, которые могут удалять проект, без проверки возможности просмотра."""
    if context.user.has_perm('dcis.delete_project') or (
            obj.user_id == context.user.id and
            context.user.has_perm('dcis.add_project') and
            obj.period_set.count() == 0
    ):
        return
    raise PermissionDenied('Недостаточно прав для удаления проекта')


# class DeleteProjectBase(BasePermission):
#     """Пропускает пользователей, которые могут удалять проект, без проверки возможности просмотра."""
#
#     @staticmethod
#     def has_object_permission(context, obj):
#         return context.user.has_perm('dcis.delete_project') or (
#                 obj.user_id == context.user.id and
#                 context.user.has_perm('dcis.add_project') and
#                 obj.period_set.count() == 0
#         )


def can_delete_project(context, obj: Project):
    """Пропускает пользователей, которые могут просматривать и удалять проект."""
    can_view_project(context, obj)
    can_delete_project_base(context, obj)


# class DeleteProject(BasePermission):
#     """Пропускает пользователей, которые могут просматривать и удалять проект."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Project):
#         can_view_project(context, obj)
#         return DeleteProjectBase.has_object_permission(
#             context, obj
#         )
