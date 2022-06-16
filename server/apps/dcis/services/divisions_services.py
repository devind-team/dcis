"""Модуль, отвечающий за выгрузку дивизионов пользователей."""

from typing import Optional
from devind_helpers.orm_utils import get_object_or_none
from graphql_relay import from_global_id
from apps.core.models import User
from apps.dcis.models import Project


def get_user_divisions(user: User, project_id: Optional[str]) -> list[dict[str, str]]:
    project: Optional[Project] = None \
        if project_id is None \
        else get_object_or_none(Project, pk=from_global_id(project_id)[1])
    return user.divisions(project)
