# Generated by Django 3.2.14 on 2022-08-03 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0021_add_document_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='protected',
            field=models.BooleanField(default=True, help_text='Является ли статус защищенным от изменения'),
        ),
        migrations.AlterField(
            model_name='status',
            name='edit',
            field=models.BooleanField(default=False, help_text='Можно ли редактировать документ со статусом'),
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(help_text='Название статуса', max_length=250),
        ),
    ]