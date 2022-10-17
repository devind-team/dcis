from typing import Type, Callable, Any

from django.core.exceptions import PermissionDenied


def is_raises(exception: Type[BaseException], func: Callable[..., Any], *args, **kwargs) -> bool:
    try:
        func(*args, **kwargs)
    except (exception,):
        return True
    else:
        return False


def check_permission_wrapper(permission_function: Callable[..., None], *args, **kwargs) -> bool:
    """Обертка над пермишеннами."""
    try:
        permission_function(*args, **kwargs)
        return True
    except PermissionDenied:
        return False
