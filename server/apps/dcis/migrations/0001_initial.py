# Generated by Django 3.2.12 on 2022-03-10 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('devind_core', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование атрибута', max_length=100)),
                ('placeholder', models.CharField(help_text='Подсказка', max_length=100)),
                ('key', models.CharField(help_text='Ключ', max_length=30)),
                ('kind', models.PositiveIntegerField(choices=[(0, 'text'), (1, 'money')], default=0, help_text='Тип атрибута')),
                ('default', models.TextField(help_text='Значение по умолчанию')),
                ('mutable', models.BooleanField(default=True, help_text='Можно ли изменять')),
                ('parent', models.ForeignKey(help_text='Родительские данные для сбора', null=True, on_delete=django.db.models.deletion.CASCADE, to='dcis.attribute')),
            ],
            options={
                'ordering': ('key', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horizontal_align', models.PositiveIntegerField(choices=[(0, 'left'), (1, 'center'), (2, 'right')], default=0, help_text='Горизонтальное выравнивание')),
                ('vertical_align', models.PositiveIntegerField(choices=[(0, 'top'), (1, 'bottom'), (2, 'middle')], default=2, help_text='Вертикальное выравнивание')),
                ('size', models.PositiveIntegerField(default=12, help_text='Размер шрифта')),
                ('strong', models.BooleanField(default=False, help_text='Жирный шрифт')),
                ('italic', models.BooleanField(default=False, help_text='Курсив')),
                ('strike', models.BooleanField(default=False, help_text='Зачеркнутый')),
                ('underline', models.PositiveIntegerField(choices=[(0, 'none'), (1, 'single'), (2, 'double'), (3, 'single_accounting'), (4, 'double_accounting')], default=0, help_text='Тип подчеркивания')),
                ('color', models.CharField(max_length=7, default='#000000', help_text='Цвет индекса')),
                ('background', models.CharField(max_length=7, default='#FFFFFF', help_text='Цвет фона')),
                ('kind', models.PositiveIntegerField(choices=[(0, 'text'), (1, 'computing'), (2, 'money'), (3, 'date'), (4, 'datetime'), (5, 'file')], default=0, help_text='Тип значения')),
                ('formula', models.TextField(help_text='Формула', null=True)),
                ('comment', models.TextField(help_text='Комментарий', null=True)),
                ('default', models.TextField(help_text='Значение по умолчанию', null=True)),
                ('mask', models.TextField(help_text='Маска для ввода значений', null=True)),
                ('tooltip', models.TextField(help_text='Подсказка', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ColumnDimension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horizontal_align', models.PositiveIntegerField(choices=[(0, 'left'), (1, 'center'), (2, 'right')], default=0, help_text='Горизонтальное выравнивание')),
                ('vertical_align', models.PositiveIntegerField(choices=[(0, 'top'), (1, 'bottom'), (2, 'middle')], default=2, help_text='Вертикальное выравнивание')),
                ('size', models.PositiveIntegerField(default=12, help_text='Размер шрифта')),
                ('strong', models.BooleanField(default=False, help_text='Жирный шрифт')),
                ('italic', models.BooleanField(default=False, help_text='Курсив')),
                ('strike', models.BooleanField(default=False, help_text='Зачеркнутый')),
                ('underline', models.PositiveIntegerField(choices=[(0, 'none'), (1, 'single'), (2, 'double'), (3, 'single_accounting'), (4, 'double_accounting')], default=0, help_text='Тип подчеркивания')),
                ('color', models.PositiveIntegerField(default=65, help_text='Цвет индекса')),
                ('background', models.PositiveIntegerField(default=65, help_text='Цвет фона')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('index', models.PositiveIntegerField(default=0, help_text='Индекс колонки')),
                ('width', models.PositiveIntegerField(help_text='Ширина колонки', null=True)),
                ('fixed', models.BooleanField(default=False, help_text='Фиксация колонки')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ('index', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(help_text='Комментарий', max_length=1023)),
                ('version', models.PositiveIntegerField(default=0, help_text='Версия документа')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Дата обновления')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ('-version', '-created_at'),
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование периода', max_length=250)),
                ('status', models.PositiveIntegerField(choices=[(0, 'preparation'), (1, 'open'), (2, 'close')], default=0, help_text='Статус проекта')),
                ('multiple', models.BooleanField(default=False, help_text='Множественное заполнение')),
                ('start', models.DateTimeField(help_text='Дата начала', null=True)),
                ('expiration', models.DateTimeField(help_text='Дата окончания', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Дата обновления')),
                ('methodical_support', models.ManyToManyField(help_text='Методическая поддержка', to='devind_core.File')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Privilege',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование привилегии', max_length=250)),
                ('key', models.CharField(help_text='Ключ привилегии', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания')),
            ],
            options={
                'ordering': ('key', 'id'),
            },
        ),
        migrations.CreateModel(
            name='RowDimension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horizontal_align', models.PositiveIntegerField(choices=[(0, 'left'), (1, 'center'), (2, 'right')], default=0, help_text='Горизонтальное выравнивание')),
                ('vertical_align', models.PositiveIntegerField(choices=[(0, 'top'), (1, 'bottom'), (2, 'middle')], default=2, help_text='Вертикальное выравнивание')),
                ('size', models.PositiveIntegerField(default=12, help_text='Размер шрифта')),
                ('strong', models.BooleanField(default=False, help_text='Жирный шрифт')),
                ('italic', models.BooleanField(default=False, help_text='Курсив')),
                ('strike', models.BooleanField(default=False, help_text='Зачеркнутый')),
                ('underline', models.PositiveIntegerField(choices=[(0, 'none'), (1, 'single'), (2, 'double'), (3, 'single_accounting'), (4, 'double_accounting')], default=0, help_text='Тип подчеркивания')),
                ('color', models.PositiveIntegerField(default=65, help_text='Цвет индекса')),
                ('background', models.PositiveIntegerField(default=65, help_text='Цвет фона')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('index', models.PositiveIntegerField(default=0, help_text='Индекс строки')),
                ('height', models.PositiveIntegerField(help_text='Высота колонки', null=True)),
                ('dynamic', models.BooleanField(default=False, help_text='Динамическая ли строка')),
                ('aggregation', models.CharField(choices=[('MIN', 'min'), ('MAX', 'max')], default=None, help_text='Агрегирование перечисление (мин, макс) для динамических строк', max_length=3, null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('document', models.ForeignKey(help_text='Документ, для динамических строк', null=True, on_delete=django.db.models.deletion.CASCADE, to='dcis.document')),
                ('parent', models.ForeignKey(help_text='Родительское правило', on_delete=django.db.models.deletion.CASCADE, to='dcis.rowdimension')),
            ],
            options={
                'ordering': ('index', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование', max_length=250)),
                ('position', models.PositiveIntegerField(default=0, help_text='Позиция')),
                ('comment', models.TextField(help_text='Комментарий', max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Дата обновления')),
                ('period', models.ForeignKey(help_text='Период', on_delete=django.db.models.deletion.CASCADE, to='dcis.period')),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование статуса', max_length=250)),
                ('edit', models.BooleanField(default=False, help_text='Можно ли редактировать')),
                ('comment', models.TextField(help_text='Комментарий', null=True)),
            ],
            options={
                'ordering': ('name', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(help_text='Значение')),
                ('verified', models.BooleanField(default=True, help_text='Валидно ли поле')),
                ('error', models.CharField(help_text='Текст ошибки', max_length=255, null=True)),
                ('column', models.ForeignKey(help_text='Колонка', on_delete=django.db.models.deletion.CASCADE, to='dcis.columndimension')),
                ('document', models.ForeignKey(help_text='Документ', on_delete=django.db.models.deletion.CASCADE, to='dcis.document')),
                ('row', models.ForeignKey(help_text='Строка', on_delete=django.db.models.deletion.CASCADE, to='dcis.rowdimension')),
                ('sheet', models.ForeignKey(help_text='Лист', on_delete=django.db.models.deletion.CASCADE, to='dcis.sheet')),
            ],
        ),
        migrations.AddField(
            model_name='rowdimension',
            name='sheet',
            field=models.ForeignKey(help_text='Лист', on_delete=django.db.models.deletion.CASCADE, to='dcis.sheet'),
        ),
        migrations.AddField(
            model_name='rowdimension',
            name='user',
            field=models.ForeignKey(help_text='Пользователь', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование проекта', max_length=250)),
                ('short', models.CharField(help_text='Сокращенное наименование проекта', max_length=30)),
                ('description', models.TextField(help_text='Описание проекта', max_length=1023)),
                ('visibility', models.BooleanField(default=True, help_text='Видимость проекта')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Дата обновления')),
                ('user', models.ForeignKey(help_text='Организатор сборов', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='PeriodPrivilege',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.ForeignKey(help_text='Период', on_delete=django.db.models.deletion.CASCADE, to='dcis.period')),
                ('privilege', models.ForeignKey(help_text='Привилегия', on_delete=django.db.models.deletion.CASCADE, to='dcis.privilege')),
                ('user', models.ForeignKey(help_text='Пользователь', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование группы периода привилегии', max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания')),
                ('period', models.ForeignKey(help_text='Период', on_delete=django.db.models.deletion.CASCADE, to='dcis.period')),
                ('privileges', models.ManyToManyField(help_text='Период группы привилегии', to='dcis.Privilege')),
                ('users', models.ManyToManyField(help_text='Пользователи', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name', '-created_at'),
            },
        ),
        migrations.AddField(
            model_name='period',
            name='project',
            field=models.ForeignKey(help_text='Проект сборов', on_delete=django.db.models.deletion.CASCADE, to='dcis.project'),
        ),
        migrations.AddField(
            model_name='period',
            name='user',
            field=models.ForeignKey(help_text='Организатор сборов', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MergedCell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_col', models.IntegerField(help_text='Начальная позиция в колонке')),
                ('min_row', models.IntegerField(help_text='Начальная позиция в строке')),
                ('max_col', models.IntegerField(help_text='Конечная позиция в колонке')),
                ('max_row', models.IntegerField(help_text='Конечная позиция в строке')),
                ('sheet', models.ForeignKey(help_text='Лист', on_delete=django.db.models.deletion.CASCADE, to='dcis.sheet')),
            ],
        ),
        migrations.CreateModel(
            name='Limitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator', models.CharField(choices=[('AND', 'and'), ('OR', 'or')], default='AND', help_text='Оператор', max_length=3)),
                ('condition', models.PositiveIntegerField(choices=[(0, '<'), (1, '>'), (2, '='), (3, '<='), (4, '>=')], default=2, help_text='Состояние')),
                ('value', models.TextField(help_text='Значение')),
                ('meta', models.ForeignKey(help_text='Ячейка', on_delete=django.db.models.deletion.CASCADE, to='dcis.cell')),
                ('parent', models.ForeignKey(help_text='Родительское правило', on_delete=django.db.models.deletion.CASCADE, to='dcis.limitation')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(help_text='Комментарий', max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания')),
                ('document', models.ForeignKey(help_text='Документ', on_delete=django.db.models.deletion.CASCADE, to='dcis.document')),
                ('status', models.ForeignKey(help_text='Статус', on_delete=django.db.models.deletion.CASCADE, to='dcis.status')),
                ('user', models.ForeignKey(help_text='Пользователь', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddField(
            model_name='document',
            name='sheet',
            field=models.ManyToManyField(to='dcis.Sheet'),
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('period', models.ForeignKey(help_text='Период', on_delete=django.db.models.deletion.CASCADE, to='dcis.period')),
            ],
        ),
        migrations.AddField(
            model_name='columndimension',
            name='sheet',
            field=models.ForeignKey(help_text='Лист', on_delete=django.db.models.deletion.CASCADE, to='dcis.sheet'),
        ),
        migrations.AddField(
            model_name='columndimension',
            name='user',
            field=models.ForeignKey(help_text='Пользователь', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cell',
            name='column',
            field=models.ForeignKey(help_text='Колонка', on_delete=django.db.models.deletion.CASCADE, to='dcis.columndimension'),
        ),
        migrations.AddField(
            model_name='cell',
            name='row',
            field=models.ForeignKey(help_text='Строка', on_delete=django.db.models.deletion.CASCADE, to='dcis.rowdimension'),
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(help_text='Значение')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Дата обновления')),
                ('attribute', models.ForeignKey(help_text='Атрибут', on_delete=django.db.models.deletion.CASCADE, to='dcis.attribute')),
                ('document', models.ForeignKey(help_text='Документ', on_delete=django.db.models.deletion.CASCADE, to='dcis.document')),
            ],
        ),
        migrations.AddField(
            model_name='attribute',
            name='period',
            field=models.ForeignKey(help_text='Период', on_delete=django.db.models.deletion.CASCADE, to='dcis.period'),
        ),
        migrations.AddIndex(
            model_name='value',
            index=models.Index(fields=['document', 'sheet'], name='dcis_value_documen_49d7bb_idx'),
        ),
        migrations.AddIndex(
            model_name='value',
            index=models.Index(fields=['document', 'sheet', 'column', 'row'], name='dcis_value_documen_92ad90_idx'),
        ),
        migrations.AddIndex(
            model_name='sheet',
            index=models.Index(fields=['period', 'position'], name='dcis_sheet_period__501da3_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='periodprivilege',
            unique_together={('period', 'user', 'privilege')},
        ),
        migrations.AddIndex(
            model_name='documentstatus',
            index=models.Index(fields=['document', 'status', 'user'], name='dcis_docume_documen_d1c509_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='documentstatus',
            unique_together={('document', 'status')},
        ),
        migrations.AddIndex(
            model_name='document',
            index=models.Index(fields=['content_type', 'object_id'], name='dcis_docume_content_ff0c1c_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='document',
            unique_together={('version', 'content_type', 'object_id')},
        ),
        migrations.AddIndex(
            model_name='division',
            index=models.Index(fields=['content_type', 'object_id'], name='dcis_divisi_content_18f5d6_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='columndimension',
            unique_together={('index', 'sheet')},
        ),
        migrations.AddIndex(
            model_name='cell',
            index=models.Index(fields=['column', 'row'], name='dcis_cell_column__8f42fa_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='cell',
            unique_together={('column', 'row')},
        ),
        migrations.AddIndex(
            model_name='attributevalue',
            index=models.Index(fields=['document', 'attribute'], name='dcis_attrib_documen_1378f7_idx'),
        ),
    ]
