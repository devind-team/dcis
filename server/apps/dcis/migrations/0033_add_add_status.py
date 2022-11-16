# Generated by Django 3.2.16 on 2022-10-31 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0032_sheet_limitation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='protected',
        ),
        migrations.CreateModel(
            name='AddStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roles', models.JSONField(help_text='Роли пользователей, которые могут изменять статус')),
                ('check', models.CharField(help_text='Функция, проверяющая может ли статус быть изменен', max_length=250)),
                ('from_status', models.ForeignKey(help_text='Изначальный статус', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_add_statuses', to='dcis.status')),
                ('to_status', models.ForeignKey(help_text='Новый статус', on_delete=django.db.models.deletion.CASCADE, related_name='to_add_statuses', to='dcis.status')),
            ],
        ),
    ]