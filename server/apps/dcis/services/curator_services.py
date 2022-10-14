from apps.dcis.models import CuratorGroup
from devind_helpers.orm_utils import get_object_or_404



def add_curator_group(name: str) -> CuratorGroup:
    """Добавление кураторской группы."""
    return CuratorGroup.objects.create(name=name)

def delete_curator_group(curator_group_id: str | int) -> str | int:
    """Удаление кураторской группы."""
    curator_group: CuratorGroup = get_object_or_404(CuratorGroup, pk=curator_group_id)
    curator_group.delete()
    return curator_group_id
