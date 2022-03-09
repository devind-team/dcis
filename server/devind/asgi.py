import os
from django.conf.urls import url
from django.core.asgi import get_asgi_application
from .celery import app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devind.settings')
django_asgi_app = get_asgi_application()


from devind_core.middleware import TokenAuthMiddleware    # noqa
from channels.routing import ProtocolTypeRouter, URLRouter   # noqa
from .ws_consumer import GraphqlWsConsumer  # noqa

app.set_default()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': TokenAuthMiddleware(
        URLRouter([
            url(r'^graphql/$', GraphqlWsConsumer.as_asgi())
        ])
    ),
})
