from pprint import pprint
from django.db import reset_queries, connection
from django.http import HttpRequest, HttpResponse


class DatabaseRequestsMiddleware:
    """Прослойка информирующая от запросов."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        reset_queries()
        response: HttpResponse = self.get_response(request)
        pprint(len(connection.queries))
        print(connection.queries)
        return  response
