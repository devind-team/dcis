# Модуль document_services

Тестирование модуля, отвечающего за работу с документами.

## Класс GetUserDocumentsTestCase

Тестирование получения документов пользователя.

### Методы

| Сигнатура                                                         | Декораторы | Описание                                                                                                     |
| :---------------------------------------------------------------- | :--------- | :----------------------------------------------------------------------------------------------------------- |
| setUp(self) -&#62; None                                           | -          | Создание данных для тестирования.                                                                            |
| test_get_user_documents_with_global_perm(self) -&#62; None        | -          | Тестирование функции `get_user_documents`.Пользователь обладает глобальной привилегией `dcis.view_document`. |
| test_get_user_documents_with_local_perm(self) -&#62; None         | -          | Тестирование функции `get_user_documents`.Пользователь обладает локальной привилегией `view_document`.       |
| test_get_user_documents_user_is_project_creator(self) -&#62; None | -          | Тестирование функции `get_user_documents`.Пользователь является создателем проекта периода.                  |
| test_get_user_documents_user_is_period_creator(self) -&#62; None  | -          | Тестирование функции `get_user_documents`.Пользователь является создателем периода.                          |
| test_get_user_documents_multiple_period(self) -&#62; None         | -          | Тестирование функции `get_user_documents`.Для периода выбран множественный тип сбора.                        |
| test_get_user_documents_single_period(self) -&#62; None           | -          | Тестирование функции `get_user_documents`.Для периода выбран единичный тип сбора.                            |