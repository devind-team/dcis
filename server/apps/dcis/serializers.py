"""Сериализация моделей базы данных."""


from rest_framework import serializers
from apps.dcis.models import Project, Period
from apps.core.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """Сериализация модели проектов."""

    user = UserSerializer()

    class Meta:
        """Мета класс настроек."""

        model = Project
        fields = '__all__'


class PeriodSerializer(serializers.ModelSerializer):
    """Сериализация периодов."""

    project = ProjectSerializer()

    class Meta:
        """Метакласс настроек."""

        model = Period
        fields = '__all__'
