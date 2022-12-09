"""Разрешения на работу с периодами проектов."""

from django.core.exceptions import PermissionDenied

from apps.core.models import User
from apps.dcis.models import Period, Project
from apps.dcis.services.privilege_services import has_privilege
from .project_permissions import can_view_project
from ..services.curator_services import is_period_curator


def can_view_period(user: User, period: Period):
    """Пропускает пользователей, которые могут просматривать период."""
    from apps.dcis.services.period_services import get_user_periods
    can_view_project(user, period.project)
    if period in get_user_periods(user, period.project.id):
        return
    raise PermissionDenied('Недостаточно прав для просмотра периода.')


def can_add_period_base(user: User, project: Project):
    """Пропускает пользователей, которые могут добавлять периоды в проект, без проверки возможности просмотра."""
    if user.has_perm('dcis.add_period') or (
        project.user_id == user.id and
        user.has_perm('dcis.add_project')
    ):
        return
    raise PermissionDenied('Недостаточно прав для добавления периода.')


def can_add_period(user: User, project: Project):
    """Пропускает пользователей, которые могут просматривать проект и добавлять в него периоды."""
    can_view_project(user, project)
    can_add_period_base(user, project)


def can_change_period_base(user: User, period: Period):
    """Пропускает пользователей, которые могут изменять период в проекте, без проверки возможности просмотра."""
    if (
        user.has_perm('dcis.change_period') or
        period.project.user_id == user.id and user.has_perm('dcis.add_project') or
        period.user_id == user.id and user.has_perm('dcis.add_period') or
        has_privilege(user.id, period.id, 'change_period')
    ):
        return
    raise PermissionDenied('Недостаточно прав для изменения периода в проекте.')


def can_change_period(user: User, period: Period):
    """Пропускает пользователей, которые могут просматривать и изменять период в проекте."""
    can_view_period(user, period)
    can_change_period_base(user, period)


def can_change_period_divisions_base(user: User, period: Period):
    """Пропускает пользователей, которые могут изменять дивизионы периода, без проверки возможности просмотра."""
    try:
        can_change_period_base(user, period)
        return
    except PermissionDenied:
        if has_privilege(user.id, period.id, 'change_period_divisions'):
            return
    raise PermissionDenied('Недостаточно прав для изменения дивизионов периода.')


def can_change_period_divisions(user: User, period: Period):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем дивизионы."""
    can_view_period(user, period)
    can_change_period_divisions_base(user, period)


def can_change_period_limitations_base(user: User, period: Period):
    """Пропускает пользователей, которые могут изменять ограничения периода, без проверки возможности просмотра."""
    try:
        can_change_period_base(user, period)
        return
    except PermissionDenied:
        if has_privilege(user.id, period.id, 'change_period_limitations'):
            return
    raise PermissionDenied('Недостаточно прав для изменения ограничений периода.')


def can_change_period_limitations(user: User, period: Period):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем ограничения."""
    can_view_period(user, period)
    can_change_period_limitations_base(user, period)


def can_change_period_groups_base(user: User, period: Period):
    """Пропускает пользователей, которые могут изменять группы периода, без проверки возможности просмотра."""
    try:
        can_change_period_base(user, period)
        return
    except PermissionDenied:
        if has_privilege(user.id, period.id, 'change_period_groups'):
            return
    raise PermissionDenied('Недостаточно прав для изменения групп периода.')


def can_change_period_groups(user: User, period: Period):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем группы."""
    can_view_period(user, period)
    can_change_period_groups_base(user, period)


def can_change_period_users_base(user: User, period: Period):
    """Пропускает пользователей, которые могут изменять пользователей периода, без проверки возможности просмотра."""
    try:
        can_change_period_base(user, period)
        return
    except PermissionDenied:
        if has_privilege(user.id, period.id, 'change_period_users'):
            return
    raise PermissionDenied('Недостаточно прав для изменения пользователей периода.')


def can_change_period_users(user: User, period: Period):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем пользователей."""
    can_view_period(user, period)
    can_change_period_users_base(user, period)


def can_change_period_attributes_base(user: User, period: Period):
    """Пропускает пользователей, которые могут изменять атрибуты периода, без проверки возможности просмотра."""
    try:
        can_change_period_base(user, period)
        return
    except PermissionDenied:
        if has_privilege(user.id, period.id, 'change_period_attributes'):
            return
    raise PermissionDenied('Недостаточно прав для изменения атрибутов периода.')


def can_change_period_attributes(user: User, period: Period):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем атрибуты."""
    can_view_period(user, period)
    can_change_period_attributes_base(user, period)


def can_view_period_report_base(user: User, period: Period):
    """Пропускает пользователей, которые могут просматривать сводный отчет периода.

    Функция не проверяет, может ли пользователь просматривать период.
    """
    try:
        can_change_period_base(user, period)
        return
    except PermissionDenied:
        if is_period_curator(user, period):
            return
        if has_privilege(user.id, period.id, 'view_period_report'):
            return
    raise PermissionDenied('Недостаточно прав для просмотра сводного отчета периода.')


def can_view_period_report(user: User, period: Period):
    """Пропускает пользователей, которые могут просматривать сводный отчет периода."""
    can_view_period(user, period)
    can_view_period_report_base(user, period)


def can_change_period_settings_base(user: User, period: Period):
    """Пропускает пользователей, которые могут изменять настройки периода, без проверки возможности просмотра."""
    try:
        can_change_period_base(user, period)
        return
    except PermissionDenied:
        if has_privilege(user.id, period.id, 'change_period_settings'):
            return
    raise PermissionDenied('Недостаточно прав для изменения настроек периода.')


def can_change_period_settings(user: User, period: Period):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем настройки."""
    can_view_period(user, period)
    can_change_period_settings_base(user, period)


def can_change_period_sheet_base(user: User, period: Period):
    """Пропускает пользователей, которые могут изменять структуру листа, без проверки возможности просмотра."""
    if (
        user.has_perm('dcis.change_sheet') or
        period.project.user_id == user.id and user.has_perm('dcis.add_project') or
        period.user_id == user.id and user.has_perm('dcis.add_period') or
        has_privilege(user.id, period.id, 'change_sheet')
    ):
        return
    raise PermissionDenied('Недостаточно прав для изменения структуры листа.')


def can_change_period_sheet(user: User, period: Period):
    """Пропускает пользователей, которые могут просматривать период и изменять в нем структуру листа."""
    can_view_period(user, period)
    can_change_period_sheet_base(user, period)


def can_delete_period_base(user: User, period: Period):
    """Пропускает пользователей, которые могут удалять период, без проверки возможности просмотра."""
    if user.has_perm('dcis.delete_period') or (
        period.project.user_id == user.id and
        user.has_perm('dcis.add_project') and
        period.document_set.count() == 0
    ) or (
        period.user_id == user.id and
        user.has_perm('dcis.add_period') and
        period.document_set.count() == 0
    ):
        return
    raise PermissionDenied('Недостаточно прав для удаления периода.')


def can_delete_period(user: User, period: Period):
    """Пропускает пользователей, которые могут просматривать и удалять период в проекте."""
    can_view_period(user, period)
    can_delete_period_base(user, period)
