"""Модуль для сервисов атрибутов."""
import json
from datetime import datetime
from os.path import join
from posixpath import relpath
from typing import Any, Sequence

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.files.base import File
from django.db import transaction
from django.db.models import QuerySet
from django.template import Context, Template
from django.utils.safestring import mark_safe
from pydantic import BaseModel, ValidationError, parse_obj_as

from apps.core.models import User
from apps.dcis.helpers.pydantic_translate import translate
from apps.dcis.models import Attribute, AttributeValue, Cell, Document, Period, Value
from apps.dcis.permissions import can_change_attribute_value, can_change_period_attributes
from .value_services import UpdateOrCrateValuesResult, ValueInput, update_or_create_values


def create_attribute(
    user: User,
    period: Period,
    name: str,
    placeholder: str,
    key: str,
    kind: str,
    default: str,
    mutable: bool
) -> Attribute:
    """Сервис добавления атрибута."""
    can_change_period_attributes(user, period)
    return Attribute.objects.create(
        period=period,
        name=name,
        placeholder=placeholder,
        key=key,
        kind=kind,
        default=default,
        mutable=mutable
    )


def change_attribute(
    user: User,
    attribute: Attribute,
    name: str,
    placeholder: str,
    key: str,
    kind: str,
    default: str,
    mutable: bool
) -> Attribute:
    """Сервис изменения атрибута."""
    can_change_period_attributes(user, attribute.period)
    attribute.name = name
    attribute.placeholder = placeholder
    attribute.key = key
    attribute.kind = kind
    attribute.default = default
    attribute.mutable = mutable
    attribute.save()
    return attribute


def change_attribute_value(
    user: User,
    attribute: Attribute,
    document: Document,
    value: str
) -> tuple[AttributeValue, Sequence[Value]]:
    """Сервис изменения значений атрибута.

    Кроме этого, необходимо собрать контекст из существующих атрибутов и перерендерить.
    """
    try:
        can_change_attribute_value(user, document, attribute)
    except PermissionDenied as error:
        raise PermissionDenied({'value': str(error)})

    attribute_value, _ = AttributeValue.objects.update_or_create(
        document=document,
        attribute=attribute, defaults={
            'value': value
        }
    )
    context: Context = create_attribute_context(user, document)
    values: Sequence[Value] = rerender_values(user, document, context)
    return attribute_value, values


def rerender_values(user: User, document: Document, context: Context) -> Sequence[Value]:
    """Функция для ререндера параметров."""
    sheet_ids = document.sheets.values_list('id', flat=True)
    cells = Cell.objects.filter(
        is_template=True,
        column__sheet__in=sheet_ids,
        row__sheet__in=sheet_ids
    ).select_related('column').all()
    values: list[Value] = []
    for cell in cells:
        value = Template(cell.default).render(context)
        changed_values: UpdateOrCrateValuesResult = update_or_create_values(
            user=user,
            document=document,
            sheet_id=cell.column.sheet_id,
            value_inputs=[ValueInput(cell=cell, value=value)]
        )
        values.append(*changed_values.values)
    return values


def create_attribute_context(user: User, document: Document) -> Context:
    """Функция для создания контекста."""
    attributes: QuerySet[Attribute] = Attribute.objects.filter(period=document.period).all()
    attribute_values: dict[int, str] = {
        attribute_value['attribute_id']: attribute_value['value']
        for attribute_value in AttributeValue.objects.filter(document=document).values('attribute_id', 'value')
    }
    context: dict[str, str] = {
        attribute.key: mark_safe(attribute_values.get(attribute.id, attribute.default))
        for attribute in attributes
    }
    # Расширяем контекст с помощью встроенных переменных
    context.update(
        {
            'user': mark_safe(user.get_full_name),
            'org_id': mark_safe(document.object_id),
            'org_name': mark_safe(document.object_name)
        }
    )
    return Context(context)


class AttributeFromJsonFile(BaseModel):
    """Вспомогательный класс для загрузки атребутов через json файл."""
    name: str
    placeholder: str
    key: str
    kind: str
    default: str
    mutable: bool


@transaction.atomic()
def upload_attributes_from_file(user: User, period: Period, attributes_file: File) -> list[Attribute]:
    """Функция загрузки атребутов периода через json файл."""

    can_change_period_attributes(user, period)

    Attribute.objects.filter(period=period).delete()

    try:
        data = parse_obj_as(list[AttributeFromJsonFile], json.load(attributes_file))
    except json.JSONDecodeError as e:
        raise ValueError(f'Неверный формат JSON: {e.msg}.')
    except ValidationError as error:
        e = translate.translate(error.errors(), locale="ru_RU")
        raise ValueError(f"Недопустимые данные JSON: запись {e[0]['loc'][1] + 1} {e[0]['msg']} {e[0]['loc'][2]}.")

    return [
        Attribute.objects.create(
            name=attribute.name,
            placeholder=attribute.placeholder,
            key=attribute.key,
            kind=attribute.kind,
            default=attribute.default,
            mutable=attribute.mutable,
            period=period
        ) for attribute in data
    ]


def unload_attributes_in_file(user: User, get_host: Any | None, period: Period) -> str:
    """Выгрузка атребутов периода в json файл."""

    can_change_period_attributes(user, period)

    data = [
        dict(
            AttributeFromJsonFile(
                name=attribute.name,
                placeholder=attribute.placeholder,
                key=attribute.key,
                kind=attribute.kind,
                default=attribute.default,
                mutable=attribute.mutable
            )
        )
        for attribute in Attribute.objects.filter(period=period)
    ]

    path = join(
        settings.STATICFILES_DIRS[1],
        'temp_files',
        f'period_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.json'
    )
    with open(path, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    return relpath(path, settings.BASE_DIR)
