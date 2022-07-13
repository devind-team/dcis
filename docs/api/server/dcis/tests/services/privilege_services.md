# Модуль privilege_services

Тесты модуля, отвечающего за работу с привилегиями.

## Класс PrivilegeServicesTestCase

Тесты модуля, отвечающего за работу с привилегиями.

### Методы

| Сигнатура                                       | Декораторы | Описание                                         |
| :---------------------------------------------- | :--------- | :----------------------------------------------- |
| setUp(self) -&#62; None                         | -          | Создание данных для тестирования.                |
| test_has_individual_privilege(self) -&#62; None | -          | Тестирование функции `has_individual_privilege`. |
| test_has_group_privilege(self) -&#62; None      | -          | Тестирование функции `has_group_privilege`.      |
| test_has_privilege(self) -&#62; None            | -          | Тестирование функции `has_privilege`             |