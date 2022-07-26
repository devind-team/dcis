"""Разрешения на работу с периодами проектов."""

from django.core.exceptions import PermissionDenied


from apps.dcis.models import Period, Project
from apps.dcis.services.period_services import get_user_periods
from apps.dcis.services.privilege_services import has_privilege
from .project_permissions import can_view_project


def can_view_period(context, obj: Period):
    """Пропускает пользователей, которые могут просматривать период."""
    can_view_project(
        context, obj.project
    )
    if obj in get_user_periods(context.user, obj.project.id):
        return
    raise PermissionDenied('Недостаточно прав для просмотра периода')


# class ViewPeriod(BasePermission):
#     """Пропускает пользователей, которые могут просматривать период."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         can_view_project(
#             context, obj.project
#         )
#         return obj in get_user_periods(
#             context.user,
#             obj.project.id
#         )


def can_add_period_base(context, obj: Project):
    """Пропускает пользователей, которые могут добавлять периоды в проект, без проверки возможности просмотра."""
    if context.user.has_perm('dcis.add_period') or (
        obj.user_id == context.user.id and
        context.user.has_perm('dcis.add_project')
    ):
        return
    raise PermissionDenied('Недостаточно прав для добавления периода')


# class AddPeriodBase(BasePermission):
#     """Пропускает пользователей, которые могут добавлять периоды в проект, без проверки возможности просмотра."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Project):
#         return context.user.has_perm('dcis.add_period') or (
#             obj.user_id == context.user.id and
#             context.user.has_perm('dcis.add_project')
#         )

def can_add_period(context, obj: Project):
    """Пропускает пользователей, которые могут просматривать проект и добавлять в него периоды."""
    can_view_project(context, obj)
    can_add_period_base(context, obj)

# class AddPeriod(BasePermission):
#     """Пропускает пользователей, которые могут просматривать проект и добавлять в него периоды."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Project):
#         can_view_project(
#             context, obj
#         )
#         return AddPeriodBase.has_object_permission(
#             context, obj
#         )

def can_change_period_base(context, obj: Period):
    """Пропускает пользователей, которые могут изменять период в проекте, без проверки возможности просмотра."""
    if (
        context.user.has_perm('dcis.change_period') or
        obj.project.user_id == context.user.id and context.user.has_perm('dcis.add_project') or
        obj.user_id == context.user.id and context.user.has_perm('dcis.add_period') or
        has_privilege(context.user.id, obj.id, 'change_period')
    ):
        return
    raise PermissionDenied('Недостаточно прав для изменения периода в проекте')

# class ChangePeriodBase(BasePermission):
#     """Пропускает пользователей, которые могут изменять период в проекте, без проверки возможности просмотра."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return (
#             context.user.has_perm('dcis.change_period') or
#             obj.project.user_id == context.user.id and context.user.has_perm('dcis.add_project') or
#             obj.user_id == context.user.id and context.user.has_perm('dcis.add_period') or
#             has_privilege(context.user.id, obj.id, 'change_period')
#         )


def can_change_period(context, obj: Period):
    """Пропускает пользователей, которые могут просматривать и изменять период в проекте."""
    can_view_period(context, obj)
    can_change_period_base(context, obj)


# class ChangePeriod(BasePermission):
#     """Пропускает пользователей, которые могут просматривать и изменять период в проекте."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return ViewPeriod.has_object_permission(
#             context, obj
#         ) and ChangePeriodBase.has_object_permission(
#             context, obj
#         )

def can_change_period_divisions_base(context, obj: Period):
    """Пропускает пользователей, которые могут изменять дивизионы периода, без проверки возможности просмотра."""
    try:
        can_change_period_base(context, obj)
        return
    except PermissionDenied:
        if has_privilege(context.user.id, obj.id, 'change_period_divisions'):
            return
    raise PermissionDenied('Недостаточно прав для изменения дивизионов в периоде')



# class ChangePeriodDivisionsBase(BasePermission):
#     """Пропускает пользователей, которые могут изменять дивизионы периода, без проверки возможности просмотра."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return ChangePeriodBase.has_object_permission(
#             context, obj
#         ) or has_privilege(
#             context.user.id, obj.id, 'change_period_divisions'
#         )

def can_change_period_divisions(context, obj: Period):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем дивизионы."""
    can_view_period(context, obj)
    can_change_period_divisions_base(context, obj)

# class ChangePeriodDivisions(BasePermission):
#     """Пропускает пользователей, которые могут просматривать период и изменять в нем дивизионы."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return ViewPeriod.has_object_permission(
#             context, obj
#         ) and ChangePeriodDivisionsBase.has_object_permission(
#             context, obj
#         )

def can_change_period_groups_base(context, obj: Period):
    """Пропускает пользователей, которые могут изменять группы периода, без проверки возможности просмотра."""
    try:
        can_change_period_base(context, obj)
        return
    except PermissionDenied:
        if has_privilege(context.user.id, obj.id, 'change_period_groups'):
            return
    raise PermissionDenied('Недостаточно прав для изменения групп периода')


# class ChangePeriodGroupsBase(BasePermission):
#     """Пропускает пользователей, которые могут изменять группы периода, без проверки возможности просмотра."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return ChangePeriodBase.has_object_permission(
#             context, obj
#         ) or has_privilege(
#             context.user.id, obj.id, 'change_period_groups'
#         )


def can_change_period_groups(context, obj: Period):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем группы."""
    can_view_period(context, obj)
    can_change_period_groups_base(context, obj)


# class ChangePeriodGroups(BasePermission):
#     """Пропускает пользователей, которые могут просматривать период и изменять в нем группы."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return ViewPeriod.has_object_permission(
#             context, obj
#         ) and ChangePeriodGroupsBase.has_object_permission(
#             context, obj
#         )

def can_change_period_users_base(context, obj: Period):
    """Пропускает пользователей, которые могут изменять пользователей периода, без проверки возможности просмотра."""
    try:
        can_change_period_base(context, obj)
        return
    except PermissionDenied:
        if has_privilege(context.user.id, obj.id, 'change_period_users'):
            return
    raise PermissionDenied('Недостаточно прав для изменения пользователей периода')


# class ChangePeriodUsersBase(BasePermission):
#     """Пропускает пользователей, которые могут изменять пользователей периода, без проверки возможности просмотра."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return ChangePeriodBase.has_object_permission(
#             context, obj
#         ) or has_privilege(
#             context.user.id, obj.id, 'change_period_users'
#         )

def can_change_period_users(context, obj: Period):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем пользователей."""
    can_view_period(context, obj)
    can_change_period_users_base(context, obj)


# class ChangePeriodUsers(BasePermission):
#     """Пропускает пользователей, которые могут просматривать период и изменять в нем пользователей."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return ViewPeriod.has_object_permission(
#             context, obj
#         ) and ChangePeriodUsersBase.has_object_permission(
#             context, obj
#         )

def can_change_period_settings_base(context, obj: Period):
    """Пропускает пользователей, которые могут изменять настройки периода, без проверки возможности просмотра."""
    try:
        can_change_period_base(context, obj)
        return
    except PermissionDenied:
        if has_privilege(context.user.id, obj.id, 'change_period_settings'):
            return
    raise PermissionDenied('Недостаточно прав для изменения настроек периода')

# class ChangePeriodSettingsBase(BasePermission):
#     """Пропускает пользователей, которые могут изменять настройки периода, без проверки возможности просмотра."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return ChangePeriodBase.has_object_permission(
#             context, obj
#         ) or has_privilege(
#             context.user.id, obj.id, 'change_period_settings'
#         )

def can_change_period_settings(context, obj: Period):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем настройки."""
    can_view_period(context, obj)
    can_change_period_settings_base(context, obj)

# class ChangePeriodSettings(BasePermission):
#     """Пропускает пользователей, которые могут просматривать период и изменять в нем настройки."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return ViewPeriod.has_object_permission(
#             context, obj
#         ) and ChangePeriodSettingsBase.has_object_permission(
#             context, obj
#         )

def can_change_period_sheet_base(context, obj: Period):
    """Пропускает пользователей, которые могут изменять структуру листа, без проверки возможности просмотра."""
    if (
        context.user.has_perm('dcis.change_sheet') or
        obj.project.user_id == context.user.id and context.user.has_perm('dcis.add_project') or
        obj.user_id == context.user.id and context.user.has_perm('dcis.add_period') or
        has_privilege(context.user.id, obj.id, 'change_sheet')
    ):
        return
    raise PermissionDenied('Недостаточно прав для изменения структуры листа')

# class ChangePeriodSheetBase(BasePermission):
#     """Пропускает пользователей, которые могут изменять структуру листа, без проверки возможности просмотра."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return (
#             context.user.has_perm('dcis.change_sheet') or
#             obj.project.user_id == context.user.id and context.user.has_perm('dcis.add_project') or
#             obj.user_id == context.user.id and context.user.has_perm('dcis.add_period') or
#             has_privilege(context.user.id, obj.id, 'change_sheet')
#         )

def can_change_period_sheet(context, obj: Period):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем структуру листа."""
    can_view_period(context, obj)
    can_change_period_sheet_base(context, obj)

# class ChangePeriodSheet(BasePermission):
#     """Пропускает пользователей, которые могут просматривать период и изменять в нем структуру листа."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return ViewPeriod.has_object_permission(
#             context, obj
#         ) and ChangePeriodSheetBase.has_object_permission(
#             context, obj
#         )

def can_delete_period_base(context, obj: Period):
    """Пропускает пользователей, которые могут удалять период, без проверки возможности просмотра."""
    if context.user.has_perm('dcis.delete_period') or (
        obj.project.user_id == context.user.id and
        context.user.has_perm('dcis.add_project') and
        obj.document_set.count() == 0
    ) or (
        obj.user_id == context.user.id and
        context.user.has_perm('dcis.add_period') and
        obj.document_set.count() == 0
    ):
        return
    raise PermissionDenied('Недостаточно прав для удаления периода')


# class DeletePeriodBase(BasePermission):
#     """Пропускает пользователей, которые могут удалять период, без проверки возможности просмотра."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return context.user.has_perm('dcis.delete_period') or (
#             obj.project.user_id == context.user.id and
#             context.user.has_perm('dcis.add_project') and
#             obj.document_set.count() == 0
#         ) or (
#             obj.user_id == context.user.id and
#             context.user.has_perm('dcis.add_period') and
#             obj.document_set.count() == 0
#         )

def can_delete_period(context, obj: Period):
    """Пропускает пользователей, которые могут просматривать и удалять период в проекте."""
    can_view_period(context, obj)
    can_delete_period_base(context, obj)

# class DeletePeriod(BasePermission):
#     """Пропускает пользователей, которые могут просматривать и удалять период в проекте."""
#
#     @staticmethod
#     def has_object_permission(context, obj: Period):
#         return ViewPeriod.has_object_permission(
#             context, obj
#         ) and DeletePeriodBase.has_object_permission(
#             context, obj
#         )
