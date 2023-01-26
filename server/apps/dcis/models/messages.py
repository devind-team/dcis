from django.db import models

from apps.core.models import User
from .document import Document


class DocumentMessage(models.Model):
    """Модель комментариев к документу"""

    MESSAGE = 'message'
    STATUS = 'status'

    KIND_DOCUMENT_MESSAGE = (
        (MESSAGE, 'message'),
        (STATUS, 'status')
    )

    comment = models.TextField(max_length=1023, help_text='Комментарий')
    kind = models.CharField(max_length=10, default=MESSAGE, choices=KIND_DOCUMENT_MESSAGE, help_text='Тип сообщения')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='Пользователь, добавивший комментарий'
    )
    document = models.ForeignKey(Document, on_delete=models.CASCADE, help_text='Документ')

    class Meta:
        ordering = ('-created_at',)
