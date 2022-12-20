"""Модуль, отвечающий за выгрузку периода."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from devind_dictionaries.models import Organization
from django.conf import settings
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from apps.core.models import User
from apps.dcis.models import Document, Period
from apps.dcis.permissions import can_view_period_result


@dataclass
class Column:
    """Выгружаемый столбец."""
    key: str
    names: list[str]


@dataclass
class DataSource:
    """Источник данных для ячейки."""
    organization: Organization
    document: Document | None
    sheet: dict[str, str]

    def __getitem__(self, item: Column) -> str:
        """Получение данных из источника."""
        value = self
        for key in item.key.split('.'):
            if value is None:
                return ''
            value = value[key] if isinstance(value, dict) else getattr(value, key)
        return value or ''


class PeriodUnload:
    """Выгрузка периода в формате Excel."""

    def __init__(self, period: Period) -> None:
        """Инициализация.
        - period - выгружаемы период
        """
        self.period = period
        self.path = Path(settings.DOCUMENTS_DIR, f'document_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.xlsx')
        self._organizations = Organization.objects.filter(
            id__in=self.period.division_set.values_list('object_id', flat=True)
        )
        self._documents = Document.objects.filter(
            period=self.period,
            object_id__in=self._organizations.values_list('id', flat=True)
        )
        self._documents_map: dict[int, Document | None] | None = None
        self._columns: list[Column] | None = None

    @property
    def documents_map(self) -> dict[int, Document | None]:
        """Отображение идентификаторов организаций на документы."""
        if self._documents_map is None:
            self._documents_map = self._build_documents_map()
        return self._documents_map

    @property
    def columns(self) -> list[Column]:
        """Выгружаемые столбцы."""
        if self._columns is None:
            self._columns = self._build_columns()
        return self._columns

    @property
    def header_size(self) -> int:
        """Размер шапки таблицы."""
        return max(len(column.names) for column in self.columns)

    def unload(self) -> str:
        """Выгрузка."""
        workbook = Workbook()
        workbook.remove(workbook.active)
        for sheet in self.period.sheet_set.all():
            worksheet = workbook.create_sheet(sheet.name)
            self._save_columns(worksheet)
            self._save_rows(worksheet)
        workbook.save(self.path)
        return f'/{self.path.relative_to(settings.BASE_DIR)}'

    def _save_columns(self, worksheet: Worksheet) -> None:
        """Сохранение название столбцов на лист Excel."""
        for column_index, column in enumerate(self.columns, 1):
            for row_index, name in enumerate(column.names, 1):
                worksheet.cell(row=row_index, column=column_index, value=name)

    def _save_rows(self, worksheet: Worksheet) -> None:
        """Сохранение строки на лист Excel."""
        row_index = self.header_size + 1
        for organization in self._organizations:
            document = self.documents_map[organization.id]
            data_source = DataSource(organization=organization, document=document, sheet={})
            for column_index, column in enumerate(self.columns, 1):
                worksheet.cell(row=row_index, column=column_index, value=data_source[column])
            row_index += 1

    def _build_documents_map(self) -> dict[int, Document | None]:
        """Отображение идентификаторов организаций на документы."""
        result: dict[int, Document | None] = {}
        for organization in self._organizations:
            result[organization.id] = next(
                (document for document in self._documents if organization.id == document.object_id),
                None
            )
        return result

    @staticmethod
    def _build_columns() -> list[Column]:
        """Построение столбцов."""
        columns = [
            Column(key='organization.attributes.idlistedu', names=['IdListEdu']),
            Column(key='organization.parent.attributes.idlistedu', names=['id_parent']),
            Column(key='organization.kodbuhg', names=['Бухкод']),
            Column(key='organization.region.common_id', names=['Код региона']),
            Column(key='organization.region.name', names=['Регион']),
            Column(key='organization.name', names=['Название учреждения']),
            Column(key='organization.parent.name', names=['Название головного учреждения']),
            Column(key='document.last_status.status.name', names=['Статус документа']),
            Column(key='organization.kind', names=['Тип организации']),
        ]
        return columns


def unload_period(user: User, period: Period) -> str:
    """Выгрузка периода в формате Excel."""
    can_view_period_result(user, period)
    return PeriodUnload(period).unload()
