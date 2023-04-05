# Generated by Django 3.2.18 on 2023-03-23 13:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0043_delete_extra_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addstatus',
            name='check',
            field=models.CharField(default='', help_text='Действие при добавлении статуса в документ', max_length=250),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='addstatus',
            old_name='check',
            new_name='action',
        ),
        migrations.AddField(
            model_name='documentstatus',
            name='archive_period',
            field=models.ForeignKey(
                help_text='Архивированный период',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='dcis.period'
            ),
        ),
        migrations.AddField(
            model_name='period',
            name='archive',
            field=models.BooleanField(default=False, help_text='Архивный период'),
        ),
        migrations.AlterField(
            model_name='cell',
            name='color',
            field=models.CharField(default='#000000', help_text='Цвет текста', max_length=16),
        ),
        migrations.AlterField(
            model_name='document',
            name='sheets',
            field=models.ManyToManyField(help_text='Листы документа', to='dcis.Sheet'),
        ),
    ]