import os

from django.db import models

from .project import Period


def period_directory_path(instance, filename: str):
    """Формируем автоматический путь директории методических рекомендаций."""
    return f'storage/period_methodical_support/{instance.period.id}/{filename}'


class PeriodMethodicalSupport(models.Model):
    """Класс для описания модели методических рекомендаций."""

    name = models.CharField(max_length=255, help_text='Название файла')
    src = models.FileField(upload_to=period_directory_path, help_text='Путь к файлу')
    deleted = models.BooleanField(default=False, help_text='Помечаем удаленный файл')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата добавления файла')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления файла')

    period = models.ForeignKey(
        Period,
        null=True,
        on_delete=models.CASCADE,
        help_text='Период'
    )

    class Meta:
        """Мета класс модели для методических рекомендаций."""

        ordering = ('-created_at',)

    @property
    def ext(self) -> str:
        """Расширение файла."""
        return os.path.splitext(self.src.path)[1]

    @property
    def size(self) -> float:
        """Размер файла в байтах, кБайт = 1 байт * 1024."""
        return os.path.getsize(self.src.path) if os.path.isfile(self.src.path) else -1.
