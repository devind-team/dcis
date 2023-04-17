from devind_dictionaries.models import Organization
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.dcis.models import Period, PeriodMethodicalSupport, Project
from apps.dcis.models.methodical_support import file_directory_path
from apps.dcis.tests.tests_helpers import create_in_memory_file


class PeriodMethodicalSupportModelTestCase(TestCase):
    """Тестирование модели PeriodMethodicalSupport"""

    def setUp(self) -> None:
        """Создание данных для тестирования."""

        self.organization_content_type = ContentType.objects.get_for_model(Organization)
        self.project = Project.objects.create(content_type=self.organization_content_type)
        self.period = Period.objects.create(project=self.project)
        self.file = create_in_memory_file('test_create_period.xlsx')
        self.period_methodical_support = PeriodMethodicalSupport.objects.create(
            period=self.period,
            name=self.file.name,
            src=self.file
        )

    def test_period_methodical_support_src(self) -> None:
        """Тестирование свойства src."""
        self.assertEqual(
            self.period_methodical_support.src,
            file_directory_path(self.period_methodical_support, self.file.name)
        )
