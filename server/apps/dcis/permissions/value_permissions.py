from devind_helpers.permissions import BasePermission

from apps.dcis.models import Document
from apps.dcis.services.divisions_services import document_in_user_divisions


class ChangeValue(BasePermission):
    """Пропускает пользователей, которые могут изменять значение ячейки в документе."""

    @staticmethod
    def has_object_permission(context, obj: Document):
        return context.user.has_perm('dcis.change_value') or document_in_user_divisions(obj, context.user)
