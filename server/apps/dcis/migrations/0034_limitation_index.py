# Generated by Django 3.2.16 on 2022-11-08 22:17

from django.db import migrations, models


def set_index(apps, schema_editor):
    """Добавление индекса к ограничению, накладываемому на лист."""
    Period = apps.get_model('dcis', 'Period')
    Limitation = apps.get_model('dcis', 'Limitation')
    for period in Period.objects.all():
        limitations = Limitation.objects.filter(sheet__in=period.sheet_set.all()).order_by('id')
        for i, limitation in enumerate(limitations, 1):
            limitation.index = i
        Limitation.objects.bulk_update(limitations, ['index'])


def empty_reverse(apps, schema_editor):
    """Пустая функция для отката миграции, т.к. поле `set_index` является вычисляемым."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0033_add_add_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='limitation',
            options={'ordering': ('index',)},
        ),
        migrations.AddField(
            model_name='limitation',
            name='index',
            field=models.PositiveSmallIntegerField(default=1, help_text='Индекс, начиная с 1, для вывода и расчета'),
            preserve_default=False,
        ),
        migrations.RunPython(set_index, empty_reverse)
    ]
