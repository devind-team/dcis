from django.core.exceptions import PermissionDenied

from apps.core.models import User


def can_add_curator_group(user: User):
    """Пропускает пользователей, которые могут добавлять кураторскую группу."""
    if user.has_perm('dcis.add_curatorgroup'):
        return
    raise PermissionDenied('Недостаточно прав для добавления кураторской группы.')


def can_change_curator_group(user: User):
    """Пропускает пользователей, которые могут изменять кураторскую группу."""
    if user.has_perm('dcis.change_curatorgroup'):
        return
    raise PermissionDenied('Недостаточно прав для изменения кураторской группы.')


def can_delete_curator_group(user: User):
    """Пропускает пользователей, которые могут изменять кураторскую группу."""
    if user.has_perm('dcis.delete_curatorgroup'):
        return
    raise PermissionDenied('Недостаточно прав для изменения кураторской группы.')
