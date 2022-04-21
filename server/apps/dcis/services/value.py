from os import path
from pathlib import Path
from typing import cast
from zipfile import ZipFile

from devind_core.models import File
from django.conf import settings

from apps.dcis.models import Value


def get_file_value_payload(value: Value) -> list[int]:
    """Получение дополнительных данных значения ячейки типа `Файл`."""
    if value.payload is None:
        return []
    return cast(list[int], value.payload)


def get_file_value_files(value: Value) -> list[File]:
    """Получение файлов значения ячейки типа `Файл`."""
    payload = get_file_value_payload(value)
    files = File.objects.filter(pk__id=payload)
    return sorted(files, key=lambda file: payload.index(file.pk))


def get_file_value_archive_url(value: Value) -> str:
    """Получение url архива значения ячейки типа `Файл`."""
    archive_path = path.join(settings.TEMP_FILES_DIR, value.value)
    with ZipFile(archive_path, 'w') as zip_file:
        for file in get_file_value_files(value):
            zip_file.write(file.src.path)
    return f'/{Path(path.relpath(archive_path, settings.BASE_DIR)).as_posix()}'
