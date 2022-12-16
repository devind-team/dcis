# Generated by Django 3.2.16 on 2022-12-08 11:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dcis', '0037_change_sort_attributes'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(help_text='Комментарий', max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания')),
                ('document', models.ForeignKey(help_text='Документ', on_delete=django.db.models.deletion.CASCADE, to='dcis.document')),
                ('user', models.ForeignKey(help_text='Пользователь, добавивший комментарий', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]