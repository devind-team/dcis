"""Файл сериализации пользователей."""

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя."""

    class Meta:
        """Мета класс настроек."""

        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name'
        )
