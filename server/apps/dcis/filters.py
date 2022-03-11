from graphene_django_filter import AdvancedFilterSet

from .models import Project


class ProjectFilter(AdvancedFilterSet):

    class Meta:
        model = Project
        fields = {
            'name': ['icontains'],
            'user': ['exact', 'in']
        }