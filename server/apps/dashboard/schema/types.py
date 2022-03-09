"""Описание возвращаемых типов."""

import graphene
from graphene_django.types import ObjectType


class PointStatisticsType(ObjectType):
    """Информация по показателям для типов различных показателей."""

    name = graphene.String(required=True, description='Название')
    value = graphene.Int(required=True, description='Текущее значение')


class PointTotalStatisticsType(PointStatisticsType):
    """Точка статистики."""

    total = graphene.Int(required=True, description='Общее значение')


class DateStatisticsType(ObjectType):
    """Информация по показателям во временной развертке."""

    date = graphene.Date(required=True, description='Дата')
    value = graphene.Float(required=True, description='Значение')


class RequestStatisticsType(ObjectType):
    """Информация по клиентам, с которых делаются запросы."""

    browsers = graphene.List(PointStatisticsType, required=True, description='Клиенты')
    os = graphene.List(PointStatisticsType, required=True, description='Операционные системы')
    device = graphene.List(PointStatisticsType, required=True, description='Устройства')


class ActiveStatisticsType(ObjectType):
    """Информация активности пользователей и времени ответа браузеров."""

    times = graphene.List(DateStatisticsType, required=True, description='Время ответа сервера')
    queries = graphene.List(DateStatisticsType, required=True, description='Запросы')
