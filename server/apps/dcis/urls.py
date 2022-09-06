"""Пути для внешней интеграции."""

from django.urls import path
from apps.dcis.views import ProjectsView, PeriodsView, get_divisions


urlpatterns = [
    path('projects', ProjectsView.as_view()),
    path('periods', PeriodsView.as_view()),
    path('divisions/<int:period_id>/', get_divisions)
]
