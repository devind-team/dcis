# Модуль period_services

Тесты модуля, отвечающего за работу с периодами.

## Класс GetUserPeriodsTestCase

Тестирование получения периодов пользователя.

### Методы

| Сигнатура                                                                       | Декораторы | Описание                                                                                               |
| :------------------------------------------------------------------------------ | :--------- | :----------------------------------------------------------------------------------------------------- |
| setUp(self) -&#62; None                                                         | -          | Создание данных для тестирования.                                                                      |
| test_get_user_participant_periods_user_is_project_creator(self) -&#62; None     | -          | Тестирование функции `get_user_participant_periods`, если пользователь является создателем проекта.    |
| test_get_user_participant_periods_user_is_not_project_creator(self) -&#62; None | -          | Тестирование функции `get_user_participant_periods`, если пользователь не является создателем проекта. |
| test_user_privileges_periods(self) -&#62; None                                  | -          | Тестирование функции `get_user_privileges_periods`.                                                    |
| test_get_user_divisions_periods_without_periods(self) -&#62; None               | -          | Тестирование функции `get_user_divisions_periods` для пользователя, у которого нет периодов.           |
| test_get_user_divisions_periods_with_periods(self) -&#62; None                  | -          | Тестирование функции `get_user_divisions_periods` для пользователя, у которого есть периоды.           |
| test_user_periods_with_perm(self) -&#62; None                                   | -          | Тестирование функции `get_user_periods` при наличии у пользователя разрешения `dcis.view_period`.      |
| test_user_periods_without_perm(self) -&#62; None                                | -          | Тестирование функции `get_user_periods` при отсутствии у пользователя разрешения `dcis.view_period`.   |