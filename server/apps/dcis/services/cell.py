from typing import Tuple, List, Optional
from devind_helpers.schema.types import ErrorFieldType
from devind_helpers.utils import convert_str_to_int, convert_str_to_bool


def check_cell_options(field: str, value: str) -> Tuple[bool, Optional[List[ErrorFieldType]]]:
    allow_fields: List[str] = ['horizontal_align', 'vertical_align', 'size', 'strong', 'italic', 'underline', 'kind']
    if field not in allow_fields:
        return False, [ErrorFieldType(
            'field',
            [f'Параметр не в списке разрешенных: {field}. {", ".join(allow_fields)}']
        )]
    if field == 'horizontal_align':
        allow_horizontal_align: List[str] = ['left', 'center', 'right']
        if value not in allow_horizontal_align:
            return False, [ErrorFieldType(
                'value',
                [f'Значение не в списке разрешенных: {field} -> {", ".join(allow_horizontal_align)}']
            )]
        return True, None
    if field == 'vertical_align':
        allow_vertical_align: List[str] = ['top', 'middle', 'bottom']
        if value not in allow_vertical_align:
            return False, [ErrorFieldType(
                'value',
                [f'Значение не в списке разрешенных: {field} -> {", ".join(allow_vertical_align)}']
            )]
        return True, None
    if field == 'size':
        value: Optional[int] = convert_str_to_int(value)
        if not value:
            return False, [ErrorFieldType(
                'value',
                [f'Разрешены только цифры.']
            )]
        if 10 <= value <= 24:
            return False, [ErrorFieldType(
                'value',
                [f'Разрешенный диапазон: 10 <= {value} <= 24.']
            )]
        return True, None
    if field in ['strong', 'italic', 'underline']:
        value: Optional[bool] = convert_str_to_bool(value)
        if not value:
            return False, [ErrorFieldType(
                'value',
                [f'Разрешены значения: "yes", "true", "t", "y", "1", "no", "false", "f", "n", "0".']
            )]
        return True, None