# Generated by Django 3.2.13 on 2022-04-25 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0013_add_value_payload'),
    ]

    operations = [
        migrations.AddField(
            model_name='columndimension',
            name='kind',
            field=models.CharField(choices=[('n', 'n'), ('s', 's'), ('f', 'f'), ('b', 'b'), ('inlineStr', 'inlineStr'), ('e', 'e'), ('str', 'str'), ('d', 'd'), ('text', 'text'), ('money', 'money'), ('bigMoney', 'bigMoney'), ('fl', 'fl'), ('user', 'user'), ('department', 'department'), ('organization', 'organization'), ('classification', 'classification')], default='s', help_text='Тип значения', max_length=30),
        ),
        migrations.AlterField(
            model_name='cell',
            name='kind',
            field=models.CharField(choices=[('n', 'n'), ('s', 's'), ('f', 'f'), ('b', 'b'), ('inlineStr', 'inlineStr'), ('e', 'e'), ('str', 'str'), ('d', 'd'), ('text', 'text'), ('money', 'money'), ('bigMoney', 'bigMoney'), ('fl', 'fl'), ('user', 'user'), ('department', 'department'), ('organization', 'organization'), ('classification', 'classification')], default='s', help_text='Тип значения', max_length=30),
        ),
    ]
