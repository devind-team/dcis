"""Пути для внешней интеграции."""

from django.urls import path
from apps.dcis.views import ProjectView


urlpatterns = [
    path('projects', ProjectView.as_view())
]
