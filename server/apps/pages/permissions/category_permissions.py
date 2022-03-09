from apps.pages.models import Category
from devind_helpers.permissions import BasePermission, ModelPermission

AddCategory = ModelPermission('pages.add_category')
ChangeAbsoluteCategory = ModelPermission('pages.change_category')


class ChangeCategory(BasePermission):
    """Пропускает пользователей, которые могут изменять категорию"""

    @staticmethod
    def has_object_permission(context, obj: Category):
        return context.user.has_perm('pages.change_category') or obj.user == context.user


class DeleteCategory(BasePermission):
    """Пропускает пользователей, которые могут удалять категории"""

    @staticmethod
    def has_object_permission(context, obj: Category):
        return context.user.has_perm('pages.delete_category') or obj.user == context.user
