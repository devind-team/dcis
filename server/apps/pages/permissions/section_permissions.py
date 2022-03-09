from apps.pages.models import Page, Section
from devind_helpers.permissions import BasePermission


class AddSection(BasePermission):
    """Пропускает пользователей, которые могут добавлять секции на страницу"""

    @staticmethod
    def has_object_permission(context, obj: Page):
        return context.user.has_perm('pages.add_section') or obj.user == context.user


class ChangeSection(BasePermission):
    """Пропускает пользователей, которые могут изменять секцию"""

    @staticmethod
    def has_object_permission(context, section: Section):
        return context.user.has_perm('pages.change_section') \
            or section.user == context.user \
            or section.page.user == context.user


class DeleteSection(BasePermission):
    """Пропускает пользователей, которые могут удалять секцию"""

    @staticmethod
    def has_object_permission(context, section: Section):
        return context.user.has_perm('pages.delete_section') \
            or section.user == context.user \
            or section.page.user == context.user
