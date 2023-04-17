"""Общая логика для тестирования сервисов."""

from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Period, Project, Sheet


class TableTestCase(TestCase):
    """Общие данные для тестирования колонок и строк."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.department_content_type = ContentType.objects.get_for_model(Department)

        self.project = Project.objects.create(content_type=self.department_content_type)
        self.period = Period.objects.create(project=self.project)
        self.sheet = Sheet.objects.create(period=self.period)
