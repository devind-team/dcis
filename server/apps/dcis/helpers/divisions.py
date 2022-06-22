"""Вспомогательные функции для работы с дивизионами."""

from apps.core.models import User
from apps.dcis.models import Project
from apps.dcis.schema.types import DivisionModelType
from apps.dcis.services.divisions_services import get_user_divisions


def get_user_division_ids(user: User, project: Project | int | None = None) -> dict[str, int]:
    """
    Функция получает идентификаторы дивизионов с привязкой к моделям
    :param user: Пользователь
    :param project: Проект
    :return: {'department': [...], 'organization': [...]}
    """
    user_divisions: list[dict[str, str | int]] = get_user_divisions(user, project)
    divisions: dict[str, DivisionModelType] = {
        division_name: [
            user_division['id'] for user_division in user_divisions if user_division['model'] == division_name
        ]
        for division_name in Project.DIVISION_KIND.keys()
    }
    return {dn: dv for dn, dv in divisions.items() if dv}
