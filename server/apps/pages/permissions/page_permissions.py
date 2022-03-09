from apps.pages.models import Page
from devind_helpers.permissions import BasePermission, ModelPermission

AddPage = ModelPermission('pages.add_page')


class ChangePage(BasePermission):
    """Пропускает пользователей, которые могут изменять страницу"""

    @staticmethod
    def has_object_permission(context, obj: Page):
        return context.user.has_perm('pages.change_page') or obj.user == context.user


class DeletePage(BasePermission):
    """Пропускает пользователей, которые могут удалять страницу"""

    @staticmethod
    def has_object_permission(context, obj: Page):
        return context.user.has_perm('pages.delete_page') or obj.user == context.user
