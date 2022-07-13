# Модуль document_permissions

Тесты разрешений на работу с документами периодов.

## Класс DocumentPermissionsTestCase

Тесты разрешений на работу с документами периодов.

### Методы

| Сигнатура                                         | Декораторы | Описание                                      |
| :------------------------------------------------ | :--------- | :-------------------------------------------- |
| setUp(self) -&#62; None                           | -          | Создание данных для тестирования.             |
| test_view_document(self) -&#62; None              | -          | Тестирование класса `ViewDocument`.           |
| test_add_document(self) -&#62; None               | -          | Тестирование класса `AddDocument`.            |
| test_change_document(self) -&#62; None            | -          | Тестирование класса `ChangeDocument`.         |
| test_delete_document(self) -&#62; None            | -          | Тестирование класса `DeleteDocument`.         |
| test_change_value(self) -&#62; None               | -          | Тестирование класса `ChangeValue`.            |
| test_add_child_row_dimension(self) -&#62; None    | -          | Тестирование класса `AddChildRowDimension`.   |
| test_delete_child_row_dimension(self) -&#62; None | -          | Тестирование класса `DeleteChildRowDimension` |