from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from devind_core.models import LogEntry
from devind_notifications.models import Notice
from devind_notifications.tasks import send_notifications
from .models import Page


@receiver(post_save, sender=Page)
def handle_page(sender, instance: Page, **kwargs):
    LogEntry.logging(sender, instance, **kwargs)
    notice: Notice = Notice.objects.create(
        kind=Notice.PAGE,
        payload=instance.title,
        object_id=instance.pk,
        user=instance.user
    )
    send_notifications.delay(notice_id=notice.id)


@receiver(post_delete, sender=Page)
def handle_page(sender, instance: Page, **kwargs):
    LogEntry.logging(sender, instance, **kwargs)
