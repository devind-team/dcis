from auditlog.registry import auditlog

from django.dispatch import receiver
from django.db.models.signals import post_save

from devind_notifications.models import Notice
from devind_notifications.tasks import send_notifications
from .models import Page

auditlog.register(Page)


@receiver(post_save, sender=Page)
def handle_page(instance: Page, **kwargs):
    notice: Notice = Notice.objects.create(
     kind=Notice.PAGE,
     payload=instance.title,
     object_id=instance.pk,
     user=instance.user
    )
    send_notifications.delay(notice_id=notice.id)
