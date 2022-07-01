# Модуль divisions_services

Модуль, отвечающий за выгрузку дивизионов пользователей.

### Функции

| Сигнатура                                                                                                                               | Декораторы | Описание                                                                        |
| :-------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :------------------------------------------------------------------------------ |
| get_user_divisions( user: apps.core.models.User, project: apps.dcis.models.project.Project | int | None = None) -> list[dict[str, str]] | -          | Получение списка обобщенных дивизионов для пользователя user и проекта project. |
| document_in_user_divisions( document: apps.dcis.models.document.Document, user: apps.core.models.User) -> bool                          | -          | Принадлежит ли документ одному из дивизионов пользователя.                      |
| _get_division(instances) -> list[dict[str, str]]                                                                                        | -          | Получение списка обобщенных дивизионов.                                         |