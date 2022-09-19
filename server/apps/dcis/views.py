"""Модуль описания внешних запросов."""

from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Period, Project
from .serializers import PeriodSerializer, ProjectSerializer


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


@api_view(['get'])
def get_divisions(request: Request, period_id: int) -> Response:
    period: Period = get_object_or_404(Period, pk=period_id)
    divisions = period.project.division.objects \
        .filter(pk__in=period.division_set.values_list('object_id', flat=True)) \
        .values('id', 'name')
    return Response({
        '$type': period.project.content_type.model,
        'divisions': divisions
    })
