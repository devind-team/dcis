# Generated by Django 3.2.12 on 2022-03-17 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0003_auto_20220315_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='archive',
            field=models.BooleanField(default=False, help_text='Архив'),
        ),
    ]
