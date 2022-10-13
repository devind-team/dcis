"""Модуль, отвечающий за работу со статусами."""

from apps.core.models import User
from apps.dcis.models import Document, DocumentStatus, Status
from apps.dcis.permissions import (
    can_add_document_status, can_change_document,
)


def add_document_status(user: User, document: Document, status: Status, comment: str, ) -> DocumentStatus:
    """Добавление статуса документа."""
    can_add_document_status(user, document, status)
    return DocumentStatus.objects.create(
        user=user,
        document=document,
        status=status,
        comment=comment,
    )


def delete_document_status(user: User, status: DocumentStatus) -> None:
    """Удаление статуса документа."""
    can_change_document(user, status.document)
    status.delete()
