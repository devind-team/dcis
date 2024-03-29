# Generated by Django 3.2.18 on 2023-04-20 08:59

from django.db import migrations, models
from openpyxl.cell.cell import TYPE_FORMULA

from apps.dcis.models.sheet import KindCell


def replace_formula_kind_by_numeric(apps, schema_editor):
    """Изменение типа формулы на тип числа для всех ячеек."""
    Cell = apps.get_model('dcis', 'Cell')
    for cell in Cell.objects.filter(kind=TYPE_FORMULA):
        cell.kind = KindCell.NUMERIC
        cell.save(update_fields=('kind',))


def replace_numeric_kind_by_formula(apps, schema_editor):
    """Изменение типа числа на тип формулы для ячеек, содержащих формулы."""
    Cell = apps.get_model('dcis', 'Cell')
    for cell in Cell.objects.filter(formula__isnull=False):
        cell.kind = TYPE_FORMULA
        cell.save(update_fields=('kind',))


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0046_add_period_methodical_support'),
    ]

    operations = [
        migrations.RunPython(replace_formula_kind_by_numeric, replace_numeric_kind_by_formula),
        migrations.AlterField(
            model_name='cell',
            name='kind',
            field=models.CharField(choices=[('n', 'n'), ('s', 's'), ('b', 'b'), ('inlineStr', 'inlineStr'), ('e', 'e'), ('str', 'str'), ('d', 'd'), ('time', 'time'), ('text', 'text'), ('money', 'money'), ('bigMoney', 'bigMoney'), ('fl', 'fl'), ('user', 'user'), ('department', 'department'), ('organization', 'organization'), ('classification', 'classification')], default='s', help_text='Тип значения', max_length=30),
        ),
        migrations.AlterField(
            model_name='columndimension',
            name='kind',
            field=models.CharField(choices=[('n', 'n'), ('s', 's'), ('b', 'b'), ('inlineStr', 'inlineStr'), ('e', 'e'), ('str', 'str'), ('d', 'd'), ('time', 'time'), ('text', 'text'), ('money', 'money'), ('bigMoney', 'bigMoney'), ('fl', 'fl'), ('user', 'user'), ('department', 'department'), ('organization', 'organization'), ('classification', 'classification')], default='s', help_text='Тип значения', max_length=30),
        ),
    ]
