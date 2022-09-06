"""Модуль, отвечающий за работу с колонками."""
from django.db.models import Max, Min

from apps.core.models import User
from apps.dcis.models.sheet import ColumnDimension, MergedCell
from apps.dcis.permissions import can_change_period_sheet


def change_column_dimension(
    user: User,
    column_dimension: ColumnDimension,
    width: int | None,
    hidden: bool,
    kind: str
) -> ColumnDimension:
    """Изменение колонки."""
    can_change_period_sheet(user, column_dimension.sheet.period)
    column_dimension.width = width
    column_dimension.hidden = hidden
    column_dimension.kind = kind
    column_dimension.save(update_fields=('width', 'hidden', 'kind', 'updated_at'))
    return column_dimension


def change_column_dimensions_fixed(column_dimensions: list[ColumnDimension], fixed: bool) -> list[ColumnDimension]:
    """Изменение свойства fixed у колонок.

    При изменении фиксации, фиксация также меняется у колонок, которые делят общую ячейку с колонкой.
    """
    change_columns = set()
    for column_dimension in column_dimensions:
        change_columns.update(get_relative_columns(column_dimension))
    for column_dimension in change_columns:
        column_dimension.fixed = fixed
    ColumnDimension.objects.bulk_update(change_columns, ('fixed',))
    return list(change_columns)


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
