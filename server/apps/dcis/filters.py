"""Модуль описания фильтрации внешних выгрузок."""

from django_filters import rest_framework as filters
from .models import Period


class PeriodFilter(filters.FilterSet):
    """Файл фильтрации периодов."""

    class Meta:
        """Мета класс настроек."""

        model = Period
        fields = ['project_id']
