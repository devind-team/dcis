# Generated by Django 3.2.16 on 2023-01-13 01:10

import django.db.models.deletion
from django.db import migrations, models


def set_last_status(apps, schema_editor):
    """Установка последнего статуса документа."""
    Document = apps.get_model('dcis', 'Document')
    DocumentStatus = apps.get_model('dcis', 'DocumentStatus')
    for document in Document.objects.all():
        try:
            document.last_status = document.documentstatus_set.latest('created_at')
        except DocumentStatus.DoesNotExist:
            document.last_status = None
        document.save(update_fields=('last_status',))


def empty_reverse(apps, schema_editor):
    """Пустая функция для отката миграции, т.к. поле `last_status` является вычисляемым."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0039_add_document_updated_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='last_status',
            field=models.ForeignKey(help_text='Последний статус документа', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_status_document_set', to='dcis.documentstatus'),
        ),
        migrations.RunPython(set_last_status, empty_reverse),
    ]