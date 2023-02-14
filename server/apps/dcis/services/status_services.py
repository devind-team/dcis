"""Модуль, отвечающий за работу со статусами."""
from copy import deepcopy
from dataclasses import dataclass
from typing import cast

from django.core.exceptions import ValidationError
from django.db import transaction
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
    action_class = getattr(AddStatusActions, add_status.action) if add_status.action else StatusAction
    action_class.pre_execute(document)
    status_part = f'Статус документа: {status.name}.'
    comment_part = f' {comment}' if comment else ''
    message = f'{status_part}{comment_part}'
    create_document_message(user=user, document=document, message=message, kind='status')
    document_status = DocumentStatus.objects.create(
        user=user,
        document=document,
        status=status,
        comment=comment,
    )
    action_class.post_execute(document, document_status)
    return document_status


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


def delete_document_status(user: User, status: DocumentStatus) -> None:
    """Удаление статуса документа."""
    can_delete_document_status(user, status.document)
    create_document_message(
        user=user,
        document=status.document,
        message=f'Статус документа "{status.status.name}" удалён.',
        kind='status',
    )
    status.delete()


@dataclass
class LimitationError:
    form: str
    formula: str
    error_message: str
    dependencies: str


class StatusAction:
    """Действие при добавлении статуса в документ."""

    @classmethod
    def pre_execute(cls, document: Document) -> None:
        """Проверка на возможность создания статуса.

        Метод выбрасывает ValidationError с ключом 'limitations', если добавление невозможно.
        """
        ...

    @classmethod
    def post_execute(cls, document: Document, document_status: DocumentStatus) -> None:
        """Действие, выполняемое, после создания статуса."""
        ...


class AddStatusActions:
    """Действие при добавлении статуса в документ."""

    class CheckLimitations(StatusAction):
        """Проверка ограничений, накладываемых на лист."""

        VIRTUAL_SHEET_NAME = '__virtual_sheet__'

        @classmethod
        def pre_execute(cls, document: Document) -> None:
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

    class ArchivePeriod(StatusAction):
        """Архивирование периода при добавлении статуса."""

        @classmethod
        @transaction.atomic
        def post_execute(cls, document: Document, document_status: DocumentStatus) -> None:
            old_document = deepcopy(document)
            document.period.pk = None
            document.period.save()

            document.pk = None
            document.period_id = document.period.id
            period_id = document.period.id
            document.save()

            document_status.pk = None
            document_status.document_id = document.id
            document_status.archive_period_id = period_id
            document_status.save()

            for sheet in old_document.period.sheet_set.all():
                old_sheet = deepcopy(sheet)
                in_document = sheet in old_document.sheets.all()
                sheet.pk = None
                sheet.period_id = period_id
                sheet.save()
                if in_document:
                    document.sheets.add(sheet)
                for merged_cell in old_sheet.mergedcell_set.all():
                    merged_cell.pk = None
                    merged_cell.sheet_id = sheet.id
                    merged_cell.save()
                column_dimension_set = list(old_sheet.columndimension_set.order_by('id').all())
                old_column_dimension_set = deepcopy(column_dimension_set)
                for column_dimension in column_dimension_set:
                    column_dimension.pk = None
                    column_dimension.sheet_id = sheet.id
                    column_dimension.save()
                old_archive_row_dimensions = {}
                old_row_dimensions = []
                archive_row_dimensions = []
                for row_dimension in old_sheet.rowdimension_set.all():
                    old_row_dimension = deepcopy(row_dimension)
                    old_row_dimensions.append(old_row_dimension)
                    row_dimension.pk = None
                    row_dimension.document_id = document.id
                    row_dimension.sheet_id = sheet.id
                    row_dimension.save()
                    archive_row_dimensions.append(row_dimension)
                    old_archive_row_dimensions[old_row_dimension.id] = row_dimension.id
                    cell_set = old_row_dimension.cell_set.order_by('column_id').all()
                    for cell, column_dimension, old_column_dimension in zip(
                        cell_set,
                        column_dimension_set,
                        old_column_dimension_set
                    ):
                        cell.pk = None
                        cell.row_id = row_dimension.id
                        cell.column_id = column_dimension.id
                        cell.save()
                        value = old_document.value_set.filter(
                            column_id=old_column_dimension.id,
                            row_id=old_row_dimension.id
                        ).first()
                        if value:
                            value.pk = None
                            value.row_id = row_dimension.id
                            value.column_id = column_dimension.id
                            value.sheet_id = sheet.id
                            value.document_id = document.id
                            value.save()
                for old_row, archive_row in zip(old_row_dimensions, archive_row_dimensions):
                    if old_row.parent_id:
                        archive_row.parent_id = old_archive_row_dimensions[old_row.parent_id]
                        archive_row.save(update_fields=('parent_id',))
