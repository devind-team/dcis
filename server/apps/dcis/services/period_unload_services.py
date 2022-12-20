"""Модуль, отвечающий за выгрузку периода."""

from datetime import datetime
from pathlib import Path

from django.conf import settings
from openpyxl.workbook import Workbook

from apps.core.models import User
from apps.dcis.models import Period
from apps.dcis.permissions import can_view_period_result


class PeriodUnload:
    """Выгрузка периода в формате Excel."""

    def __init__(self, period: Period) -> None:
        """Инициализация.
        - period - выгружаемы период
        """
        self.period = period
        self.path = Path(settings.DOCUMENTS_DIR, f'document_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.xlsx')

    def unload(self) -> str:
        """Выгрузка."""
        workbook = Workbook()
        workbook.remove(workbook.active)
        for sheet in self.period.sheet_set.all():
            worksheet = workbook.create_sheet(sheet.name)
            worksheet.cell(1, 1, 'test')
        workbook.save(self.path)
        return f'/{self.path.relative_to(settings.BASE_DIR)}'


def unload_period(user: User, period: Period) -> str:
    """Выгрузка периода в формате Excel."""
    can_view_period_result(user, period)
    return PeriodUnload(period).unload()
