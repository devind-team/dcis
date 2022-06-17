from apps.core.models import User
from apps.dcis.models import Period


def get_periods(user: User, project_id: int):
    """Получение периодов пользователей."""
    return Period.objects.filter(project_id=project_id).all()