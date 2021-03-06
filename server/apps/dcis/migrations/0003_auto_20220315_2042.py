# Generated by Django 3.2.12 on 2022-03-15 20:42

import apps.dcis.models.sheet
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0002_auto_20220313_0507'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='border_color',
            field=models.JSONField(default=apps.dcis.models.sheet.get_default_border, help_text='Цвет границ'),
        ),
        migrations.AddField(
            model_name='cell',
            name='border_style',
            field=models.JSONField(default=apps.dcis.models.sheet.get_default_border, help_text='Стили границ'),
        ),
    ]
