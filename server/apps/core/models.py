"""Переопределенная пользовательская модель"""

from typing import Optional

from django.db.models import Q
from devind_core.models import AbstractUser


class User(AbstractUser):
    """Переопределенная модель хранения пользователей."""

    def divisions(self, project: Optional = None) -> list[dict]:
        """Получаем дивизионы пользователя в зависимости от проекта или все."""
        from apps.dcis.models import Project

        def get_division(instances) -> list[dict]:
            """Функция, которая возвращает тип, маппенный на DivisionModelType."""
            return [{
                'id': division.id,
                'name': division.name,
                'model': division._meta.model_name      # noqa
            }
                for division in instances
            ]

        if project:
            return get_division(project.division.objects.filter(Q(users=self) | Q(user=self)).all())
        divisions: list[dict] = []
        for division_model in Project.DIVISION_KIND.values():
            all_divisions = division_model.objects.filter(Q(users=self) | Q(user=self)).all()
            divisions.extend(get_division(all_divisions))
        return divisions
