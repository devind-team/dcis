# Generated by Django 3.2.16 on 2023-03-21 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0042_move_document_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='value',
            name='extra_value',
        ),
    ]
