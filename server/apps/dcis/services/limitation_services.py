"""Модуль, отвечающий за работу с ограничениями."""

import json
from datetime import datetime
from os.path import join
from posixpath import relpath

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.db import transaction
from django.db.models import F, Max
from pydantic import BaseModel

from apps.core.models import User
from apps.dcis.helpers.limitation_formula_cache import LimitationFormulaContainerCache
from apps.dcis.models import Limitation, Period
from apps.dcis.permissions import can_change_period_limitations, can_view_period


@transaction.atomic
def add_limitations_from_file(period: Period, limitations_file: File) -> list[Limitation]:
    """Добавление ограничений, накладываемых на лист, из json файла."""
    possible_keys = ['form', 'check', 'message']
    limitations: list[Limitation] = []

    def raise_error(messages: list[str]):
        raise ValidationError(message={'limitations_file': messages})

    try:
        data = json.load(limitations_file)
        if not isinstance(data, list):
            raise_error(['json файл не содержит массив на верхнем уровне'])
        sheets = list(period.sheet_set.all())
        container_cache = LimitationFormulaContainerCache()
        for i, limitation in enumerate(data, 1):
            if not isinstance(limitation, dict):
                raise_error([f'Ограничение по номеру {i} не является объектом'])
            if list(limitation.keys()) != possible_keys:
                raise_error(
                    [
                        f'Ключи ограничения по номеру {i} должны совпадать со списком {possible_keys}'.replace("'", '"')
                    ]
                )
            sheet = next((sheet for sheet in sheets if sheet.name == limitation['form']), None)
            if sheet is None:
                raise_error([f'Не найдена форма "{limitation["form"]}" для ограничения по номеру {i}'])
            limitation = Limitation.objects.create(
                index=i,
                formula=limitation['check'],
                error_message=limitation['message'],
                sheet=sheet
            )
            limitations.append(limitation)
            container_cache.add_limitation_formula(limitation)
        container_cache.save(period_id=period.id)
    except json.JSONDecodeError as error:
        raise raise_error(['Не удалось разобрать json файл', error.msg])
    return limitations


@transaction.atomic
def update_limitations_from_file(user: User, period: Period, limitations_file: File) -> list[Limitation]:
    """Обновление ограничений, накладываемых на лист, из json файла."""
    can_change_period_limitations(user, period)
    Limitation.objects.filter(sheet__period=period).delete()
    return add_limitations_from_file(period, limitations_file)


class LimitationFromJsonFile(BaseModel):
    """Вспомогательный класс для ограничений через json файл."""
    form: str
    check: str
    message: str


def unload_limitations_in_file(user: User, period: Period) -> str:
    """Выгрузка ограничений периода в json файл."""

    can_view_period(user, period)

    data = [
        dict(
            LimitationFromJsonFile(
                form=limitation.sheet.name,
                check=limitation.formula,
                message=limitation.error_message
            )
        )
        for limitation in Limitation.objects.select_related('sheet').filter(sheet__period=period)
    ]

    path = join(
        settings.STATICFILES_DIRS[1],
        'temp_files',
        f'limitation_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.json'
    )
    with open(path, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    return relpath(path, settings.BASE_DIR)


def add_limitation(user: User, formula: str, error_message: str, sheet_id: int | str) -> Limitation:
    """Добавление ограничения, накладываемого на лист."""
    period = Period.objects.get(sheet__id=sheet_id)
    can_change_period_limitations(user, period)
    max_index = Limitation.objects.filter(sheet__period=period).aggregate(Max('index'))['index__max'] or 1
    limitation = Limitation.objects.create(
        index=max_index + 1,
        formula=formula,
        error_message=error_message,
        sheet_id=sheet_id,
    )
    container_cache = LimitationFormulaContainerCache.get(period)
    container_cache.add_limitation_formula(limitation).save()
    return limitation


def change_limitation(
    user: User,
    limitation: Limitation,
    formula: str,
    error_message: str,
    sheet_id: int | str
) -> Limitation:
    """Изменение ограничения, накладываемого на лист."""
    can_change_period_limitations(user, limitation.sheet.period)
    limitation.formula = formula
    limitation.error_message = error_message
    limitation.sheet_id = sheet_id
    limitation.save(update_fields=('formula', 'error_message', 'sheet_id'))
    container_cache = LimitationFormulaContainerCache.get(limitation.sheet.period)
    container_cache.change_limitation_formula(limitation).save()
    return limitation


@transaction.atomic
def delete_limitation(user: User, limitation: Limitation) -> int:
    """Удаления ограничения, накладываемого на лист."""
    can_change_period_limitations(user, limitation.sheet.period)
    container_cache = LimitationFormulaContainerCache.get(limitation.sheet.period)
    Limitation.objects.filter(
        sheet__period=limitation.sheet.period,
        index__gt=limitation.index
    ).update(index=F('index') - 1)
    limitation_id = limitation.id
    limitation.delete()
    container_cache.delete_limitation_formula(limitation)
    return limitation_id
