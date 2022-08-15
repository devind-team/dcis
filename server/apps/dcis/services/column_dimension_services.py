"""Модуль, отвечающий за работу с колонками."""
from django.db import transaction
from django.db.models import Max, Min

from apps.core.models import User
from apps.dcis.models.sheet import ColumnDimension, MergedCell
from apps.dcis.permissions import can_change_period_sheet


@transaction.atomic
def change_column_dimension(
    user: User,
    column_dimension: ColumnDimension,
    width: int | None,
    fixed: bool,
    hidden: bool,
    kind: str
) -> list[ColumnDimension]:
    """Изменение колонки."""
    can_change_period_sheet(user, column_dimension.sheet.period)
    column_dimensions: list[ColumnDimension] = []
    column_dimension.width = width
    column_dimension.hidden = hidden
    column_dimension.kind = kind
    column_dimension.save(update_fields=('width', 'hidden', 'kind', 'updated_at'))
    column_dimensions.append(column_dimension)
    if column_dimension.fixed != fixed:
        column_dimensions = change_column_dimension_fixed(column_dimension, fixed)
    return column_dimensions


def change_column_dimension_fixed(column_dimension: ColumnDimension, fixed: bool) -> list[ColumnDimension]:
    """Изменение свойства fixed у колонки.

    При добавлении фиксации фиксация также добавляется:
      - у колонок с меньшим индексом;
      - у колонок, которые делят общую ячейку с колонкой.
    При снятии фиксации фиксация также снимается:
      - у колонок с большим индексом;
      - у колонок, которые делят общую ячейку с колонкой.
    """
    if fixed:
        columns = ColumnDimension.objects.filter(sheet=column_dimension.sheet, index__lte=column_dimension.index)
    else:
        columns = ColumnDimension.objects.filter(
            sheet=column_dimension.sheet,
            index__gte=column_dimension.index,
            fixed=True
        )
    change_columns = list({*columns, *get_relative_columns(column_dimension)})
    for column in change_columns:
        column.fixed = fixed
    ColumnDimension.objects.bulk_update(change_columns, ('fixed',))
    return change_columns


def get_relative_columns(column_dimension: ColumnDimension) -> list[ColumnDimension]:
    """Получение колонок, которые делят общую ячейку с колонкой `column_dimension`."""
    merged_cell = MergedCell.objects.filter(
        sheet=column_dimension.sheet,
        min_col__lte=column_dimension.index,
        max_col__gte=column_dimension.index,
    )
    if merged_cell.count() == 0:
        return [column_dimension]
    min_max = merged_cell.aggregate(min=Min('min_col'), max=Max('max_col'))
    return list(ColumnDimension.objects.filter(
        sheet=column_dimension.sheet,
        index__in=range(min_max['min'], min_max['max'] + 1)
    ))
