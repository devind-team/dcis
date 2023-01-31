"""Модуль, отвечающий за работу со статусами."""
from dataclasses import dataclass
from typing import cast

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from jsonpickle import encode

from apps.core.models import User
from apps.dcis.helpers.cell import ValueState, evaluate_state, parse_coordinate, resolve_cells, resolve_evaluate_state
from apps.dcis.helpers.limitation_formula_cache import LimitationFormulaContainerCache
from apps.dcis.models import Document, Limitation, Period, Status
from apps.dcis.models.document import AddStatus, DocumentStatus
from apps.dcis.permissions import AddDocumentBase, can_add_document_status, can_delete_document_status
from apps.dcis.services.divisions_services import is_period_division_member
from apps.dcis.services.document_services import create_document_message, get_user_roles


def add_document_status(user: User, document: Document, status: Status, comment: str) -> DocumentStatus:
    """Добавление статуса документа."""
    add_status = AddStatus.objects.filter(from_status=document.last_status.status, to_status=status).first()
    can_add_document_status(user, document, add_status)
    if add_status.check:
        getattr(AddStatusCheck, add_status.check)(document)
    status_part = f'Статус документа: {status.name}.'
    comment_part = f' Комментарий: {comment}' if comment else ''
    message = f'{status_part}{comment_part}'
    create_document_message(user=user, document=document, message=message, kind='status')
    return DocumentStatus.objects.create(
        user=user,
        document=document,
        status=status,
        comment=comment,
    )


def get_initial_statuses(user: User, period: Period) -> QuerySet[Status]:
    """Получение возможных начальных статусов для нового документа периода."""
    add_statuses = AddStatus.objects.none()
    if AddDocumentBase(user, period).can_add_any_division_document:
        add_statuses |= AddStatus.objects.filter(from_status=None, roles__contains='admin')
    if is_period_division_member(user, period):
        add_statuses |= AddStatus.objects.filter(from_status=None, roles__contains='division_member')
    return Status.objects.filter(to_add_statuses__in=add_statuses)


def get_new_statuses(user: User, document: Document) -> list[Status]:
    """Получение возможных новых статусов для документа."""
    user_roles = set(get_user_roles(user, document))
    add_statuses = AddStatus.objects.filter(from_status=document.last_status.status)
    return [add_status.to_status for add_status in add_statuses if len(user_roles & set(add_status.roles)) > 0]


def delete_document_status(user: User, document: Document, status: DocumentStatus) -> None:
    """Удаление статуса документа."""
    can_delete_document_status(user, status.document)
    status.delete()
    create_document_message(user=user, document=document, message='Статус документа удалён', kind='status')


@dataclass
class LimitationError:
    form: str
    formula: str
    error_message: str
    dependencies: str


class AddStatusCheck:
    """Класс с методами, определяющими, может ли в документ быть добавлен новый статус.

    Каждый метод выбрасывает ValidationError с ключом 'limitations', если добавление невозможно.
    """
    VIRTUAL_SHEET_NAME = '__virtual_sheet__'

    @classmethod
    def check_limitations(cls, document: Document) -> None:
        """Проверка ограничений, накладываемых на лист."""
        sheets = document.sheets.all()
        limitations = Limitation.objects.filter(sheet__in=sheets)
        dependency = LimitationFormulaContainerCache.get(document.period).dependency_cache.dependency
        dependencies: set[str] = set()
        for counter in dependency.values():
            dependencies.update(counter.keys())
        cells, values = resolve_cells(sheets, document, dependencies)
        state = resolve_evaluate_state(cells, values, [])
        for i, limitation in enumerate(limitations, 1):
            error_message = limitation.error_message.replace('"', '""')
            state[f'{cls.VIRTUAL_SHEET_NAME}!A{i}'] = cast(ValueState, {
                'value': None,
                'error': None,
                'formula': f'=IF({limitation.formula}, "", "{error_message}")',
                'limitation': limitation
            })
        evaluate_result = evaluate_state(state, [cls.VIRTUAL_SHEET_NAME])
        errors: list[LimitationError] = []
        for coordinate, result_value in evaluate_result.items():
            sheet_name = parse_coordinate(coordinate)[0]
            if sheet_name == cls.VIRTUAL_SHEET_NAME:
                error: str | None = None
                if result_value['error'] is not None:
                    error = result_value['error']
                elif result_value['value'] != '':
                    error = result_value['value']
                if error is not None:
                    limitation_dependencies = dependency[coordinate.replace(f'{sheet_name}!', '')]
                    dependency_values: dict[str, str] = {}
                    for key in limitation_dependencies.keys():
                        dependency_values[key] = evaluate_result[key]['value']
                    errors.append(LimitationError(
                        form=result_value['limitation'].sheet.name,
                        formula=result_value['limitation'].formula,
                        error_message=error,
                        dependencies=encode(dependency_values).encode().decode('unicode-escape')
                    ))
        if len(errors):
            raise ValidationError(message=None, code=None, params=errors)
