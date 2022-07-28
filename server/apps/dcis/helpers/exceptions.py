from typing import Type, Callable, Any


def is_raises(exception: Type[BaseException], func: Callable[..., Any], *args, **kwargs) -> bool:
    try:
        func(*args, **kwargs)
    except (exception,):
        return True
    else:
        return False
