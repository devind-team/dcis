# Generated by Django 3.2.12 on 2022-03-23 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0006_alter_period_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='cell',
            name='kind',
            field=models.CharField(choices=[('n', 'n'), ('s', 's'), ('f', 'f'), ('b', 'b'), ('inlineStr', 'inlineStr'), ('e', 'e'), ('str', 'str'), ('d', 'd'), ('text', 'text'), ('money', 'money'), ('bigMoney', 'bigMoney'), ('fl', 'fl'), ('user', 'user'), ('department', 'department'), ('organization', 'organization')], default='s', help_text='Тип значения', max_length=30),
        ),
    ]
