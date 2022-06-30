"""Разрешения на работу с периодами проектов."""

from devind_helpers.permissions import BasePermission

from apps.dcis.models import Period, Project
from apps.dcis.permissions.project_permissions import ViewProject
from apps.dcis.services.period_services import get_user_periods
from apps.dcis.services.privilege_services import has_privilege


class ViewPeriod(BasePermission):
    """Пропускает пользователей, которые могут просматривать период."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return all((
            ViewProject.has_object_permission(context, obj.project),
            obj in get_user_periods(context.user, obj.project.id),
        ))


class AddPeriod(BasePermission):
    """Пропускает пользователей, которые могут добавлять периоды в проект."""

    @staticmethod
    def has_object_permission(context, obj: Project):
        return all((
            ViewProject.has_object_permission(context, obj),
            any((
                context.user.has_perm('dcis.add_period'),
                obj.user_id == context.user.id and context.user.has_perm('dcis.add_project'),
            ))
        ))


class ChangePeriod(BasePermission):
    """Пропускает пользователей, которые могут изменять период в проекте."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        if not ViewPeriod.has_object_permission(context, obj):
            return False
        return any((
            context.user.has_perm('dcis.change_period'),
            obj.project.user_id == context.user.id and context.user.has_perm('dcis.add_project'),
            obj.user_id == context.user.id and context.user.has_perm('dcis.add_period'),
            has_privilege(context.user.id, obj.id, 'change_period')
        ))


class ChangePeriodDivisions(ChangePeriod):
    """Пропускает пользователей, которые могут изменять дивизионы периода."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        if not ViewPeriod.has_object_permission(context, obj):
            return False
        return ChangePeriod.has_object_permission(context, obj) or has_privilege(
            context.user.id, obj.id, 'change_period_divisions'
        )


class ChangePeriodUsers(ChangePeriod):
    """Пропускает пользователей, которые могут изменять пользователей периода."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        if not ViewPeriod.has_object_permission(context, obj):
            return False
        return ChangePeriod.has_object_permission(context, obj) or has_privilege(
            context.user.id, obj.id, 'change_period_users'
        )


class ChangePeriodSettings(ChangePeriod):
    """Пропускает пользователей, которые могут изменять настройки периода."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        if not ViewPeriod.has_object_permission(context, obj):
            return False
        return ChangePeriod.has_object_permission(context, obj) or has_privilege(
            context.user.id, obj.id, 'change_period_settings'
        )


class DeletePeriod(BasePermission):
    """Пропускает пользователей, которые могут удалять период в проекте."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ViewPeriod.has_object_permission(context, obj) and any((
            context.user.has_perm('dcis.delete_period'),
            all((
                obj.project.user_id == context.user.id,
                context.user.has_perm('dcis.add_project'),
                obj.document_set.count() == 0,
            )),
            all((
                obj.user_id == context.user.id,
                context.user.has_perm('dcis.add_period'),
                obj.document_set.count() == 0,
            )),
        ))
