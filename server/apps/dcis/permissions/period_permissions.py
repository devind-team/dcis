"""Разрешения на работу с периодами проектов."""

from devind_helpers.permissions import BasePermission

from apps.dcis.models import Period, Project
from apps.dcis.services.period_services import get_user_periods
from apps.dcis.services.privilege_services import has_privilege
from .project_permissions import ViewProject


class ViewPeriod(BasePermission):
    """Пропускает пользователей, которые могут просматривать период."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ViewProject.has_object_permission(context, obj.project) and obj in get_user_periods(
            context.user,
            obj.project.id
        )


class AddPeriod(BasePermission):
    """Пропускает пользователей, которые могут добавлять периоды в проект."""

    @staticmethod
    def has_object_permission(context, obj: Project):
        return ViewProject.has_object_permission(context, obj) and (
            context.user.has_perm('dcis.add_period') or (
                obj.user_id == context.user.id and
                context.user.has_perm('dcis.add_project')
            )
        )


class ChangePeriod(BasePermission):
    """Пропускает пользователей, которые могут изменять период в проекте."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        if not ViewPeriod.has_object_permission(context, obj):
            return False
        return (
            context.user.has_perm('dcis.change_period') or
            obj.project.user_id == context.user.id and context.user.has_perm('dcis.add_project') or
            obj.user_id == context.user.id and context.user.has_perm('dcis.add_period') or
            has_privilege(context.user.id, obj.id, 'change_period')
        )


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


class ChangePeriodSheet(BasePermission):
    """Пропускает пользователей, которые могут изменять структуру листа."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        if not ViewPeriod.has_object_permission(context, obj):
            return False
        return (
            context.user.has_perm('dcis.change_sheet') or
            obj.project.user_id == context.user.id and context.user.has_perm('dcis.add_project') or
            obj.user_id == context.user.id and context.user.has_perm('dcis.add_period') or
            has_privilege(context.user.id, obj.id, 'change_sheet')
        )


class DeletePeriod(BasePermission):
    """Пропускает пользователей, которые могут удалять период в проекте."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ViewPeriod.has_object_permission(context, obj) and (
            context.user.has_perm('dcis.delete_period') or (
                obj.project.user_id == context.user.id and
                context.user.has_perm('dcis.add_project') and
                obj.document_set.count() == 0
            ) or (
                obj.user_id == context.user.id and
                context.user.has_perm('dcis.add_period') and
                obj.document_set.count() == 0
            )
        )
