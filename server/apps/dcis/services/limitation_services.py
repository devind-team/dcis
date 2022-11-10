"""Модуль, отвечающий за работу с ограничениями."""

import json

from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.db import transaction
from django.db.models import F, Max

from apps.dcis.helpers.limitation_formula_cache import LimitationFormulaContainerCache
from apps.dcis.models import Limitation, Period


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
                raise_error([
                    f'Ключи ограничения по номеру {i} должны совпадать со списком {possible_keys}'.replace("'", '"')
                ])
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
def update_limitations_from_file(period: Period, limitations_file: File) -> list[Limitation]:
    """Обновление ограничений, накладываемых на лист, из json файла."""
    Limitation.objects.filter(sheet__period=period).delete()
    return add_limitations_from_file(period, limitations_file)


def add_limitation(formula: str, error_message: str, sheet_id: int | str) -> Limitation:
    """Добавление ограничения, накладываемого на лист."""
    period = Period.objects.get(sheet__id=sheet_id)
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


def change_limitation(limitation: Limitation, formula: str, error_message: str, sheet_id: int | str) -> Limitation:
    """Изменение ограничения, накладываемого на лист."""
    limitation.formula = formula
    limitation.error_message = error_message
    limitation.sheet_id = sheet_id
    limitation.save(update_fields=('formula', 'error_message', 'sheet_id'))
    container_cache = LimitationFormulaContainerCache.get(limitation.sheet.period)
    container_cache.change_limitation_formula(limitation).save()
    return limitation


@transaction.atomic
def delete_limitation(limitation: Limitation) -> int:
    """Удаления ограничения, накладываемого на лист."""
    container_cache = LimitationFormulaContainerCache.get(limitation.sheet.period)
    Limitation.objects.filter(
        sheet__period=limitation.sheet.period,
        index__gt=limitation.index
    ).update(index=F('index') - 1)
    limitation_id = limitation.id
    limitation.delete()
    container_cache.delete_limitation_formula(limitation)
    return limitation_id
