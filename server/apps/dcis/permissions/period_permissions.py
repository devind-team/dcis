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


class AddPeriodBase(BasePermission):
    """Пропускает пользователей, которые могут добавлять периоды в проект, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: Project):
        return context.user.has_perm('dcis.add_period') or (
            obj.user_id == context.user.id and
            context.user.has_perm('dcis.add_project')
        )


class AddPeriod(BasePermission):
    """Пропускает пользователей, которые могут просматривать проект и добавлять в него периоды."""

    @staticmethod
    def has_object_permission(context, obj: Project):
        return ViewProject.has_object_permission(
            context, obj
        ) and AddPeriodBase.has_object_permission(
            context, obj
        )


class ChangePeriodBase(BasePermission):
    """Пропускает пользователей, которые могут изменять период в проекте, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return (
            context.user.has_perm('dcis.change_period') or
            obj.project.user_id == context.user.id and context.user.has_perm('dcis.add_project') or
            obj.user_id == context.user.id and context.user.has_perm('dcis.add_period') or
            has_privilege(context.user.id, obj.id, 'change_period')
        )


class ChangePeriod(BasePermission):
    """Пропускает пользователей, которые могут просматривать и изменять период в проекте."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ViewPeriod.has_object_permission(
            context, obj
        ) and ChangePeriodBase.has_object_permission(
            context, obj
        )


class ChangePeriodDivisionsBase(BasePermission):
    """Пропускает пользователей, которые могут изменять дивизионы периода, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ChangePeriodBase.has_object_permission(
            context, obj
        ) or has_privilege(
            context.user.id, obj.id, 'change_period_divisions'
        )


class ChangePeriodDivisions(BasePermission):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем дивизионы."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ViewPeriod.has_object_permission(
            context, obj
        ) and ChangePeriodDivisionsBase.has_object_permission(
            context, obj
        )


class ChangePeriodUsersBase(BasePermission):
    """Пропускает пользователей, которые могут изменять пользователей периода, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ChangePeriodBase.has_object_permission(
            context, obj
        ) or has_privilege(
            context.user.id, obj.id, 'change_period_users'
        )


class ChangePeriodUsers(BasePermission):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем пользователей."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ViewPeriod.has_object_permission(
            context, obj
        ) and ChangePeriodUsersBase.has_object_permission(
            context, obj
        )


class ChangePeriodSettingsBase(BasePermission):
    """Пропускает пользователей, которые могут изменять настройки периода, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ChangePeriodBase.has_object_permission(
            context, obj
        ) or has_privilege(
            context.user.id, obj.id, 'change_period_settings'
        )


class ChangePeriodSettings(BasePermission):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем настройки."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ViewPeriod.has_object_permission(
            context, obj
        ) and ChangePeriodSettingsBase.has_object_permission(
            context, obj
        )


class ChangePeriodSheetBase(BasePermission):
    """Пропускает пользователей, которые могут изменять структуру листа, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return (
            context.user.has_perm('dcis.change_sheet') or
            obj.project.user_id == context.user.id and context.user.has_perm('dcis.add_project') or
            obj.user_id == context.user.id and context.user.has_perm('dcis.add_period') or
            has_privilege(context.user.id, obj.id, 'change_sheet')
        )


class ChangePeriodSheet(BasePermission):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем структуру листа."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ViewPeriod.has_object_permission(
            context, obj
        ) and ChangePeriodSheetBase.has_object_permission(
            context, obj
        )


class DeletePeriodBase(BasePermission):
    """Пропускает пользователей, которые могут удалять период, без проверки возможности просмотра."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return context.user.has_perm('dcis.delete_period') or (
            obj.project.user_id == context.user.id and
            context.user.has_perm('dcis.add_project') and
            obj.document_set.count() == 0
        ) or (
            obj.user_id == context.user.id and
            context.user.has_perm('dcis.add_period') and
            obj.document_set.count() == 0
        )


class DeletePeriod(BasePermission):
    """Пропускает пользователей, которые могут просматривать и удалять период в проекте."""

    @staticmethod
    def has_object_permission(context, obj: Period):
        return ViewPeriod.has_object_permission(
            context, obj
        ) and DeletePeriodBase.has_object_permission(
            context, obj
        )
