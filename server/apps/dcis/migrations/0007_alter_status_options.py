# Generated by Django 3.2.12 on 2022-03-22 08:35

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
        migrations.AlterUniqueTogether(
            name='documentstatus',
            unique_together=set(),
        ),
        migrations.AddIndex(
            model_name='documentstatus',
            index=models.Index(fields=['document', 'status'], name='dcis_docume_documen_00c5bd_idx'),
        ),
        migrations.AlterField(
            model_name='cell',
            name='kind',
            field=models.CharField(
                choices=[('n', 'n'), ('s', 's'), ('f', 'f'), ('b', 'b'), ('inlineStr', 'inlineStr'), ('e', 'e'),
                         ('str', 'str'), ('d', 'd'), ('text', 'text'), ('money', 'money'), ('bigMoney', 'bigMoney'),
                         ('fl', 'fl'), ('user', 'user'), ('department', 'department'),
                         ('organization', 'organization')], default='s', help_text='Тип значения', max_length=30),
        ),
    ]
