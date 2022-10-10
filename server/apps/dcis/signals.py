from django.dispatch import receiver
from django.db.models import signals
from devind_helpers.utils import is_template
from apps.dcis.models import Cell


@receiver(signals.pre_save, sender=Cell)
def pre_save_cell(sender, instance: Cell, *args, **kwargs):
    if instance.kind in Cell.TEMPLATE_FIELD:
        instance.is_template = is_template(instance.default)
