"""Модуль, отвечающий за работу с дивизионами."""

from django.db.models import Q

from apps.core.models import User
from apps.dcis.models import Project, Period


def get_user_divisions(user: User, project: Project | int | str | None = None) -> list[dict[str, int | str]]:
    """Получение списка обобщенных дивизионов для пользователя и проекта.

    :param user: пользователь
    :param project: объект проекта, или идентификатор проекта, или None
    :return [{'id': int, name: 'string', 'model': 'department' | 'organization'}, ...]
    """
    if project is None:
        divisions: list[dict] = []
        for division_model in Project.DIVISION_KIND.values():
            all_divisions = division_model.objects.filter(Q(users=user) | Q(user=user)).all()
            divisions.extend(get_divisions(all_divisions))
        return divisions
    project = Project.objects.get(pk=project) if type(project) in (int, str) else project
    return get_divisions(project.division.objects.filter(Q(users=user) | Q(user=user)).all())


def get_user_division_ids(user: User, project: Project | int | str | None = None) -> dict[str, int]:
    """Получение идентификаторов дивизионов с привязкой к моделям.

    :param user: пользователь
    :param project: объект проекта, или идентификатор проекта, или None
    :return: {'department': [...], 'organization': [...]}
    """
    user_divisions = get_user_divisions(user, project)
    divisions: dict[str, list[str]] = {
        division_name: [
            user_division['id'] for user_division in user_divisions if user_division['model'] == division_name
        ]
        for division_name in Project.DIVISION_KIND.keys()
    }
    return {dn: dv for dn, dv in divisions.items() if dv}


def get_period_divisions(period: Period, search: str = '') -> list[dict[str, int | str]]:
    """Получение списка обобщенных дивизионов периода."""
    return get_divisions(period.project.division.objects.filter(
        name__contains=search,
        pk__in=period.division_set.values_list('object_id', flat=True)
    ))


def get_period_possible_divisions(
    period: Period,
    search: str = ''
) -> list[dict[str, int | str]]:
    """Получение списка возможных обобщенных дивизионов периода."""
    return get_divisions(period.project.division.objects.filter(
        name__contains=search
    ).exclude(pk__in=period.division_set.values_list('object_id', flat=True)))


def get_divisions(instances) -> list[dict[str, int | str]]:
    """Получение списка обобщенных дивизионов.

    :param instances: модель дивизиона
    :return [{'id': int, name: 'string', 'model': 'department' | 'organization'}, ...]
    """
    return [{
        'id': division.id,
        'name': division.name,
        'model': division._meta.model_name  # noqa
    } for division in instances]
