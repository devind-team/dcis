from argparse import ArgumentTypeError
from typing import Optional, Union

from devind_helpers.schema.types import ErrorFieldType
from devind_helpers.utils import convert_str_to_bool, convert_str_to_int

from apps.dcis.models import Cell


def check_cell_options(field: str, value: str) -> tuple[
    bool,
    Optional[Union[str, int, bool]],
    Optional[list[ErrorFieldType]]
]:
    """Проверяем возможность изменения значений ячеек."""
    allow_fields: list[str] = ['horizontal_align', 'vertical_align', 'size', 'strong', 'italic', 'underline', 'kind']
    if field not in allow_fields:
        return False, None, [ErrorFieldType(
            'field',
            [f'Параметр не в списке разрешенных: {field}. {", ".join(allow_fields)}']
        )]
    if field == 'horizontal_align':
        allow_horizontal_align: list[str] = ['left', 'center', 'right']
        if value not in allow_horizontal_align:
            return False, None, [ErrorFieldType(
                'value',
                [f'Значение не в списке разрешенных: {field} -> {", ".join(allow_horizontal_align)}']
            )]
        return True, value, None
    if field == 'vertical_align':
        allow_vertical_align: list[str] = ['top', 'middle', 'bottom']
        if value not in allow_vertical_align:
            return False, None, [ErrorFieldType(
                'value',
                [f'Значение не в списке разрешенных: {field} -> {", ".join(allow_vertical_align)}']
            )]
        return True, value, None
    if field == 'size':
        value: Optional[int] = convert_str_to_int(value)
        if not value:
            return False, None, [ErrorFieldType(
                'value',
                [f'Разрешены только цифры.']
            )]
        if not (6 <= value <= 24):
            return False, None, [ErrorFieldType(
                'value',
                [f'Разрешенный диапазон: 10 <= {value} <= 24.']
            )]
        return True, value, None
    if field == 'underline':
        allow_underline: list[str] = ['single', 'double', 'single_accounting', 'double_accounting']
        if value not in [None, *allow_underline]:
            return False, None, [ErrorFieldType(
                'value',
                [f'Допустимые значения: null, {", ".join(allow_underline)}']
            )]
        return True, value, None
    if field in ['strong', 'italic', 'underline']:
        try:
            value: Optional[bool] = convert_str_to_bool(value)
            return True, value if field != 'underline' else 'single', None
        except ArgumentTypeError:
            return False, None, [ErrorFieldType(
                'value',
                [f'Разрешены значения: "yes", "true", "t", "y", "1", "no", "false", "f", "n", "0".']
            )]
    if field == 'kind':
        allow_kinds = [kind[0] for kind in Cell.KIND_VALUE]
        if value not in allow_kinds:
            return False, None, [ErrorFieldType(
                'value',
                [f'Разрешенные типы: {", ".join(allow_kinds)}']
            )]
        return True, value, None
