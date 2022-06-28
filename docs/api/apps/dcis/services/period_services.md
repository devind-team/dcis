# Модуль period_services



### Функции

| Signature                                                                                                                                        | Decorator | Docstring                                    |
| :----------------------------------------------------------------------------------------------------------------------------------------------- | :-------- | :------------------------------------------- |
| get_periods(user: apps.core.models.User, project_id: int)                                                                                        | -         | Получение периодов пользователей.            |
| get_user_period_privileges( user: apps.core.models.User, period: apps.dcis.models.project.Period) -> django.db.models.query.QuerySet             | -         | Получение привилегий пользователя в периоде. |
| get_user_group_privileges( user: apps.core.models.User, period_group: apps.dcis.models.privilege.PeriodGroup) -> django.db.models.query.QuerySet | -         |                                              |