from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.conf import settings


class ExternalTokenMiddleware:
    """Прослойка для авторизации внешних запросов."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.path.startswith('/external/v1/'):
            token: str | None = request.headers.get('Authorization')
            if not token or token != settings.EXTERNAL_TOKEN:
                raise PermissionDenied()
        return self.get_response(request)
