"""Схема запросов и мутация для панели информации."""

from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Dict, List

import graphene
from django.utils.timezone import make_aware
from graphene import ResolveInfo

from devind_core.models import LogRequest, Session
from .types import ActiveStatisticsType, DateStatisticsType, PointStatisticsType, RequestStatisticsType


class Query(graphene.ObjectType):
    """Запросы для получения информации о метриках сайта."""

    request_statistics = graphene.Field(RequestStatisticsType, required=True, description='Статистика запросов')
    active_statistics = graphene.Field(ActiveStatisticsType, required=True, description='Статистика активности')

    @staticmethod
    def resolve_request_statistics(root: None, info: ResolveInfo) -> RequestStatisticsType:
        """Возвращаем статистику по использованию браузерами."""
        sessions: List[Session] = Session.objects.all()
        browser_statistics: Dict[str, int] = defaultdict(int)
        os_statistics: Dict[str, int] = defaultdict(int)
        device_statistics: Dict[str, int] = defaultdict(int)
        for session in sessions:
            browser_statistics[session.browser] += 1
            os_statistics[session.os] += 1
            device_statistics[session.device] += 1
        return RequestStatisticsType(
            browsers=[PointStatisticsType(name=name, value=value) for name, value in browser_statistics.items()],
            os=[PointStatisticsType(name=name, value=value) for name, value in os_statistics.items()],
            device=[PointStatisticsType(name=name, value=value) for name, value in device_statistics.items()]
        )

    @staticmethod
    def resolve_active_statistics(root: None, info: ResolveInfo) -> ActiveStatisticsType:
        """Возвращаем статистику за 30 последних дней по активности пользователей."""
        response_data = make_aware(datetime.now() - timedelta(days=31))
        log_requests: List[LogRequest] = LogRequest\
            .objects\
            .filter(created_at__gte=response_data)\
            .order_by('created_at').all()
        times: Dict[date, float] = defaultdict(float)
        queries: Dict[date, int] = defaultdict(int)
        for log_request in log_requests:
            times[log_request.created_at.date()] += log_request.time
            queries[log_request.created_at.date()] += 1
        return ActiveStatisticsType(
            times=[DateStatisticsType(date=d, value=time / queries[d]) for d, time in times.items()],
            queries=[DateStatisticsType(date=d, value=q) for d, q in queries.items()]
        )
