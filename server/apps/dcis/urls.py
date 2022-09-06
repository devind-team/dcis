"""Пути для внешней интеграции."""

from django.urls import path
from apps.dcis.views import ProjectsView, PeriodsView


urlpatterns = [
    path('projects', ProjectsView.as_view()),
    path('periods', PeriodsView.as_view()),
]
