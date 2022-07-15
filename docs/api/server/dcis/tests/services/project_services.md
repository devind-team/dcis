# Модуль project_services

Тесты модуля, отвечающего за работу с проектами.

## Класс GetUserProjectsTestCase

Тестирование получения проектов пользователя.

### Методы

| Сигнатура                                                           | Декораторы | Описание                                                                                               |
| :------------------------------------------------------------------ | :--------- | :----------------------------------------------------------------------------------------------------- |
| setUp(self) -&#62; None                                             | -          | Создание данных для тестирования.                                                                      |
| test_get_user_participant_projects(self) -&#62; None                | -          | Тестирование функции `get_user_participant_projects`.                                                  |
| test_get_user_privileges_projects(self) -&#62; None                 | -          | Тестирование функции `get_user_privileges_projects`.                                                   |
| test_get_user_divisions_projects_without_projects(self) -&#62; None | -          | Тестирование функции `get_user_divisions_projects` для пользователя, у которого нет проектов.          |
| test_get_user_divisions_projects_with_projects(self) -&#62; None    | -          | Тестирование функции `get_user_divisions_projects` для пользователя, у которого есть проекты.          |
| test_get_user_projects_with_perm(self) -&#62; None                  | -          | Тестирование функции `get_user_projects` при наличии у пользователя разрешения `dcis.view_project`.    |
| test_get_user_projects_without_perm(self) -&#62; None               | -          | Тестирование функции `get_user_projects` при отсутствии у пользователя разрешения `dcis.view_project`. |