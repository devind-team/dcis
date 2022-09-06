"""Модуль описания внешних запросов."""


from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from .models import Project, Period
from .serializers import ProjectSerializer, PeriodSerializer


class ProjectsView(ListAPIView):
    """Вьюха для получения списка проектов."""

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class PeriodsView(ListAPIView):
    """Вьюха для получения списка периодов."""

    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('project_id',)

