# Модуль excel_extractor_services



## Класс BuildStyle

Описание стилей

### Методы

| Signature                                                                                                                                                                                      | Decorator | Docstring           |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- | :------------------ |
| __init__( self, horizontal_align: str, vertical_align: str, size: float, strong: bool, italic: bool, strike: bool, underline: bool, color: str, background: str, border_style: dict[str, str]) | -         |                     |
| __repr__(self)                                                                                                                                                                                 | -         | Return repr(self).  |
| __eq__(self, other)                                                                                                                                                                            | -         | Return self==value. |

## Класс BuildColumnDimension

Построение колонки.

### Методы

| Signature                                                                                                             | Decorator | Docstring           |
| :-------------------------------------------------------------------------------------------------------------------- | :-------- | :------------------ |
| __init__( self, width: int, fixed: bool, hidden: bool, style: apps.dcis.services.excel_extractor_services.BuildStyle) | -         |                     |
| __repr__(self)                                                                                                        | -         | Return repr(self).  |
| __eq__(self, other)                                                                                                   | -         | Return self==value. |

## Класс BuildRowDimension

Построение строки.

### Методы

| Signature                                                                                   | Decorator | Docstring           |
| :------------------------------------------------------------------------------------------ | :-------- | :------------------ |
| __init__( self, height: int, style: apps.dcis.services.excel_extractor_services.BuildStyle) | -         |                     |
| __repr__(self)                                                                              | -         | Return repr(self).  |
| __eq__(self, other)                                                                         | -         | Return self==value. |

## Класс BuildCell

Построение ячеек.

### Методы

| Signature                                                                                                                                                                                                                                                                                                                                                                                                  | Decorator | Docstring           |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- | :------------------ |
| __init__( self, horizontal_align: str, vertical_align: str, size: float, strong: bool, italic: bool, strike: bool, underline: bool, color: str, background: str, border_style: dict[str, str], column_id: int, row_id: int, kind: str, coordinate: Optional[str] = None, formula: Optional[str] = None, comment: Optional[str] = None, default: Optional[str] = None, border_color: dict[str, str] = None) | -         |                     |
| __repr__(self)                                                                                                                                                                                                                                                                                                                                                                                             | -         | Return repr(self).  |
| __eq__(self, other)                                                                                                                                                                                                                                                                                                                                                                                        | -         | Return self==value. |

## Класс BuildMergedCell

Построение объединенных ячеек.

### Методы

| Signature                                                              | Decorator | Docstring           |
| :--------------------------------------------------------------------- | :-------- | :------------------ |
| __init__(self, min_col: int, min_row: int, max_col: int, max_row: int) | -         |                     |
| __repr__(self)                                                         | -         | Return repr(self).  |
| __eq__(self, other)                                                    | -         | Return self==value. |

## Класс BuildSheet

BuildSheet(name: str, columns_dimension: dict[int, apps.dcis.services.excel_extractor_services.BuildColumnDimension], rows_dimension: dict[int, apps.dcis.services.excel_extractor_services.BuildRowDimension], cells: list[apps.dcis.services.excel_extractor_services.BuildCell], merged_cells: list[apps.dcis.services.excel_extractor_services.BuildMergedCell])

### Методы

| Signature                                                                                                                                                                                                                                                                                                                                                                 | Decorator | Docstring           |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------- | :------------------ |
| __init__( self, name: str, columns_dimension: dict[int, apps.dcis.services.excel_extractor_services.BuildColumnDimension], rows_dimension: dict[int, apps.dcis.services.excel_extractor_services.BuildRowDimension], cells: list[apps.dcis.services.excel_extractor_services.BuildCell], merged_cells: list[apps.dcis.services.excel_extractor_services.BuildMergedCell]) | -         |                     |
| __post_init__(self)                                                                                                                                                                                                                                                                                                                                                       | -         |                     |
| __repr__(self)                                                                                                                                                                                                                                                                                                                                                            | -         | Return repr(self).  |
| __eq__(self, other)                                                                                                                                                                                                                                                                                                                                                       | -         | Return self==value. |

## Класс ExcelExtractor

Парсинг xlsx файла в структуру данных для последовательной загрузки в базу данных.

### Методы

| Signature                                                                                                                                                                                                                                                             | Decorator         | Docstring                                                                                                                                                                                                                                                                              |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| __init__(self, path: pathlib.PosixPath)                                                                                                                                                                                                                               | -                 | Инициализация.:param path - путь к файлу Excel.                                                                                                                                                                                                                                        |
| save(self, period: apps.dcis.models.project.Period)                                                                                                                                                                                                                   | -                 | Сохранение обработанного файла в базу данных.                                                                                                                                                                                                                                          |
| extract(self) -> list[apps.dcis.services.excel_extractor_services.BuildSheet]                                                                                                                                                                                         | -                 | Парсинг файла Excel.Функция создает структуру данных, которая является первоначальной обработкой.После выделения необходимых данных можно осуществлять транзакционную запись в базу данных.Структура данных может использоваться для предварительной демонстрации планируемого отчета. |
| evaluate_cells( self, sheets: list[apps.dcis.services.excel_extractor_services.BuildSheet]) -> list[apps.dcis.services.excel_extractor_services.BuildSheet]                                                                                                           | -                 | Предварительно рассчитываем значения ячеек.Excel не хранит кешированные значения, вместо этого он хранит формулы.Нам необходимо рассчитать формулы, однако значения могут быть перекрестными.Поэтому нам необходимо собирать единую структуру и каждый раз формировать модель.         |
| coordinate(sheet: str, column: int, row: int)                                                                                                                                                                                                                         | ['@staticmethod'] | Получаем координату.                                                                                                                                                                                                                                                                   |
| _ExcelExtractor__border_style( dimension: Union[openpyxl.worksheet.dimensions.RowDimension, openpyxl.worksheet.dimensions.ColumnDimension, apps.dcis.models.sheet.Cell, apps.dcis.models.sheet.MergedCell]) -> apps.dcis.services.excel_extractor_services.BuildStyle | ['@staticmethod'] | for p in ('top', 'bottom', 'left', 'right', 'diagonal', 'diagonalDown', 'diagonalUp',)                                                                                                                                                                                                 |
| _ExcelExtractor__color_transform(wb, color)                                                                                                                                                                                                                           | ['@staticmethod'] |                                                                                                                                                                                                                                                                                        |