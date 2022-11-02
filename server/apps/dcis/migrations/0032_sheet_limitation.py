# Generated by Django 3.2.16 on 2022-10-31 16:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0031_aggregation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Limitation',
        ),
        migrations.CreateModel(
            name='Limitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formula', models.TextField(help_text='Формула')),
                ('error_message', models.TextField(help_text='Сообщение ошибки')),
                ('sheet',
                 models.ForeignKey(help_text='Лист', on_delete=django.db.models.deletion.CASCADE, to='dcis.sheet')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
