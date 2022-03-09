# Оформление разрешений

1. Файловая структура.  

1.1. Разрешения должны располагаться в папке permissions каждого приложения.  
1.2. Формат названия файла: "context_permissions".

2. Оформление разрешения  

Следует избегать дублирование в разрешении функционала другого разрешения.
Пример оформления:
```python
from apps.core.helpers.permissions import BasePermission, ModelPermission

class AddPage(BasePermission):
    """Пропускает пользователей, которые могут добавлять страницы"""
    
    @staticmethod
    def has_permission(context):
        ...

    @staticmethod
    def has_object_permission(context, obj):
        ...

ChangePage = ModelPermission('pages.change_page')
DeletePage = ModelPermission('pages.delete_page')
```