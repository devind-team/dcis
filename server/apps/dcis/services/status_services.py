"""Модуль, отвечающий за работу со статусами."""
from apps.core.models import User
from apps.dcis.models import Document, DocumentStatus, Status
from apps.dcis.models.document import AddStatus
from apps.dcis.permissions import (
    can_add_document_status, can_delete_document_status,
)


def add_document_status(user: User, document: Document, status: Status, comment: str) -> DocumentStatus:
    """Добавление статуса документа."""
    add_status = AddStatus.objects.filter(from_status=document.last_status.status, to_status=status).first()
    can_add_document_status(user, document, add_status)
    if add_status.check:
        getattr(StatusCheck, add_status.check)(document)
    return DocumentStatus.objects.create(
        user=user,
        document=document,
        status=status,
        comment=comment,
    )


def delete_document_status(user: User, status: DocumentStatus) -> None:
    """Удаление статуса документа."""
    can_delete_document_status(user, status.document)
    status.delete()


class StatusCheck:
    """Класс с методами, определяющими, может ли в документ быть добавлен новый статус.

    Каждый метод выбрасывает ValueError, если добавление невозможно.
    """

    @staticmethod
    def check_limitation(document: Document) -> None:
        """Проверка ограничений, накладываемых на лист."""
        raise ValueError()
