"""Модуль описания внешних запросов."""


from rest_framework.generics import ListAPIView
from .models import Project
from .serializers import ProjectSerializer, PeriodSerializer


class ProjectView(ListAPIView):
    """Вьюха для получения списка проектов."""

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
