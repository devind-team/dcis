"""Модуль, отвечающий за работу со статусами."""
from typing import cast

from django.core.exceptions import ValidationError

from apps.core.models import User
from apps.dcis.helpers.cell import ValueState, evaluate_state, parse_coordinate, resolve_cells, resolve_evaluate_state
from apps.dcis.helpers.limitation_formula_cache import LimitationFormulaContainerCache
from apps.dcis.models import Document, DocumentStatus, Limitation, Status
from apps.dcis.models.document import AddStatus
from apps.dcis.permissions import (
    can_add_document_status, can_delete_document_status,
)


def add_document_status(user: User, document: Document, status: Status, comment: str) -> DocumentStatus:
    """Добавление статуса документа."""
    add_status = AddStatus.objects.filter(from_status=document.last_status.status, to_status=status).first()
    can_add_document_status(user, document, add_status)
    if add_status.check:
        getattr(AddStatusCheck, add_status.check)(document)
    return DocumentStatus.objects.create(
        user=user,
        document=document,
        status=status,
        comment=comment,
    )


def delete_document_status(user: User, status: DocumentStatus) -> None:
    """Удаление статуса документа."""
    can_delete_document_status(user, status.document)
    status.delete()


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
        cache_container = LimitationFormulaContainerCache.get(document.period)
        dependencies: set[str] = set()
        for counter in cache_container.dependency_cache.dependency.values():
            dependencies.update(counter.keys())
        cells, values = resolve_cells(sheets, document, dependencies)
        state = resolve_evaluate_state(cells, values, [])
        for i, limitation in enumerate(limitations, 1):
            state[f'{cls.VIRTUAL_SHEET_NAME}!A{i}'] = cast(ValueState, {
                'value': None,
                'error': None,
                'formula': f'=IF({limitation.formula}, "", "{limitation.error_message}")',
                'cell': None
            })
        evaluate_result = evaluate_state(state, [cls.VIRTUAL_SHEET_NAME])
        errors: list[str] = []
        for coordinate, result_value in evaluate_result.items():
            sheet_name = parse_coordinate(coordinate)[0]
            if sheet_name == cls.VIRTUAL_SHEET_NAME:
                if result_value['error'] is not None:
                    errors.append(result_value['error'])
                elif result_value['value'] != '':
                    errors.append(result_value['value'])
        if len(errors):
            raise ValidationError(message={'limitations': errors})
