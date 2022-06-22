from typing import Sequence

from django.db.models import Q
from apps.core.models import User
from apps.dcis.models import Period
from apps.dcis.helpers.divisions import get_user_division_ids


def get_periods(user: User, project_id: int):
    """Получение периодов пользователей."""
    if user.has_perm('dcis.view_project') and user.has_perm('dcis.view_period'):
        return Period.objects.filter(project_id=project_id).all()
    period_user_ids: Sequence[int] = Period.objects \
        .filter(Q(user=user) | Q(periodgroup__users=user)) \
        .values_list('pk', flat=True)
    divisions: dict[str, int] = get_user_division_ids(user, project_id)
    period_divisions_filter = Q()
    for division_name, division_values in divisions.items():
        period_divisions_filter |= Q(project__content_type__model=division_name, division__object_id__in=division_values)
    period_division_ids: Sequence[int] = Period.objects \
        .filter(period_divisions_filter) \
        .values_list('pk', flat=True)
    return Period.objects.filter(pk__in=[*period_user_ids, *period_division_ids]).all()