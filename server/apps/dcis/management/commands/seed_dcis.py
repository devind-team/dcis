from itertools import count

from devind_core.models import File
from devind_dictionaries.models import Department
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import connection
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

        with connection.cursor() as cursor:
            for model in (Project, Period, Sheet, ColumnDimension, RowDimension, Document, Cell, MergedCell, Value):
                model.objects.all().delete()
                cursor.execute(f'ALTER SEQUENCE {model._meta.db_table}_id_seq RESTART WITH 1;')

    def handle(self, *args, **options) -> None:
        self.clear()
        seeder = Seed.seeder()
        department = Department.objects.first()
        user = User.objects.first()
        seeder.add_entity(File, 5)
        seeder.add_entity(Project, 5)
        seeder.add_entity(Period, 5)
        number_generator = iter(count(1))
        seeder.add_entity(Sheet, 60, {
            'name': lambda ie: f'Sheet {next(number_generator)}'
        })
        seeder.add_entity(Document, 15, {
            'content_type': ContentType.objects.get_for_model(Department),
            'object_id': department.id
        })
        seeder.execute()
        for sheet in Sheet.objects.all():
            columns_dimension = [
                ColumnDimension.objects.create(
                    index=i, sheet=sheet, width=75, content_object=department, user=user
                ) for i in range(20)
            ]
            rows_dimension = [
                RowDimension.objects.create(
                    index=i, sheet=sheet, height=35, content_object=department, user=user
                ) for i in range(20)
            ]
            for column_dimension in columns_dimension:
                for row_dimension in rows_dimension:
                    Cell.objects.create(column=column_dimension, row=row_dimension)
                    Value.objects.create(
                        sheet=sheet,
                        document=sheet.document_set.first() or Document.objects.first(),
                        column=column_dimension,
                        row=row_dimension,
                        value=f'{column_dimension.index}{row_dimension.index}'
                    )
            MergedCell.objects.create(sheet=sheet, min_col=1, min_row=1, max_col=2, max_row=2)
            MergedCell.objects.create(sheet=sheet, min_col=5, max_col=7, min_row=3, max_row=6)
