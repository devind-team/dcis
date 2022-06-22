"""Модуль, отвечающий за выгрузку дивизионов пользователей."""

from django.db.models import Q

from apps.core.models import User
from apps.dcis.models import Document, Project


def get_user_divisions(user: User, project: Project | int | None = None) -> list[dict[str, str]]:
    """Получение списка обобщенных дивизионов для пользователя user и проекта project."""
    if project is None:
        divisions: list[dict] = []
        for division_model in Project.DIVISION_KIND.values():
            all_divisions = division_model.objects.filter(Q(users=user) | Q(user=user)).all()
            divisions.extend(_get_division(all_divisions))
        return divisions
    project = Project.objects.get(pk=project) if type(project) == int else project
    return _get_division(project.division.objects.filter(Q(users=user) | Q(user=user)))


def document_in_user_divisions(document: Document, user: User) -> bool:
    """Принадлежит ли документ одному из дивизионов пользователя."""
    return document.object_id in [
        division['id'] for division in get_user_divisions(user, document.period.project)
    ]


def _get_division(instances) -> list[dict[str, str]]:
    """Получение списка обобщенных дивизионов."""
    return [{
        'id': division.id,
        'name': division.name,
        'model': division._meta.model_name  # noqa
    } for division in instances]
