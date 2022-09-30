# Generated by Django 3.2.15 on 2022-09-28 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0024_auto_20220927_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='kind',
            field=models.CharField(choices=[('text', 'text'), ('money', 'money'), ('bool', 'boolean'), ('bigMoney', 'bigMoney'), ('files', 'files'), ('numeric', 'numeric'), ('date', 'date')], default='text', help_text='Тип атрибута', max_length=10),
        ),
        migrations.AddField(
            model_name='period',
            name='versioning',
            field=models.BooleanField(default=False, help_text='Множество версий'),
        ),
    ]