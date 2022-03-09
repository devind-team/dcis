"""
WSGI config for devind project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from .celery import app


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devind.settings')

app.set_default()

application = get_wsgi_application()
