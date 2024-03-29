# Generated by Django 3.2.16 on 2022-10-12 12:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('devind_dictionaries', '0004_auto_20220421_2151'),
        ('dcis', '0029_cell_is_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuratorGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование кураторской группы', max_length=250)),
                ('group', models.ForeignKey(help_text='Привилегии группы', null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group')),
                ('organization', models.ManyToManyField(help_text='Организация кураторской группы', to='devind_dictionaries.Organization')),
                ('users', models.ManyToManyField(help_text='Пользователь кураторской группы', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
