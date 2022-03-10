from devind_core.models import File
from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django_seed import Seed

from apps.core.models import User
from apps.dcis.models import (
    Cell,
    ColumnDimension,
    Document,
    MergedCell,
    Period,
    Project,
    RowDimension,
    Sheet,
    Value,
)


class Command(BaseCommand):
    """Команда для случайного заполнения приложения dcis."""

    @staticmethod
    def clear() -> None:
        """Очистка моделей."""

        Project.objects.all().delete()
        Period.objects.all().delete()
        Sheet.objects.all().delete()
        ColumnDimension.objects.all().delete()
        RowDimension.objects.all().delete()
        Document.objects.all().delete()
        Cell.objects.all().delete()
        MergedCell.objects.all().delete()
        Value.objects.all().delete()

    def handle(self, *args, **options) -> None:
        self.clear()
        seeder = Seed.seeder()
        department = Department.objects.first()
        user = User.objects.first()
        seeder.add_entity(File, 5)
        seeder.add_entity(Project, 5)
        seeder.add_entity(Period, 5)
        seeder.add_entity(Sheet, 60)
        seeder.add_entity(Document, 15, {
            'content_type': ContentType.objects.get_for_model(Department),
            'object_id': department.id
        })
        seeder.execute()
        for sheet in Sheet.objects.all():
            for i in range(20):
                column_dimension = ColumnDimension.objects.create(
                    index=i, sheet=sheet, width=75, content_object=department, user=user
                )
                row_dimension = RowDimension.objects.create(
                    index=i, sheet=sheet, height=35, content_object=department, user=user
                )
                Cell.objects.create(column=column_dimension, row=row_dimension)
                MergedCell.objects.create(sheet=sheet, min_row=1, min_col=1, max_row=2, max_col=2)
                Value.objects.create(
                    sheet=sheet,
                    document=sheet.document_set.first() or Document.objects.first(),
                    column=column_dimension,
                    row=row_dimension,
                    value=f'{column_dimension.index}{row_dimension.index}'
                )
