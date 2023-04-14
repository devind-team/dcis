"""Вспомогательные функции для работы с файлами."""

from os.path import join

from django.core.files.uploadedfile import InMemoryUploadedFile
from six import BytesIO

from devind.settings import BASE_DIR


def create_in_memory_file(file_name: str) -> InMemoryUploadedFile:
    """Создание файла в памяти."""
    with open(file=join(BASE_DIR, 'apps', 'dcis', 'tests', 'resources', file_name), mode='rb') as file:
        stream = BytesIO()
        stream.write(file.read())
        in_memory_file = InMemoryUploadedFile(
            file=stream,
            field_name=None,
            name=file.name,
            content_type=None,
            size=stream.tell(),
            charset=None
        )
        in_memory_file.seek(0)
        return in_memory_file
