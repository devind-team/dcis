from django.db import migrations, models


def move_document_status_comments(apps, schema_editor):
    """Перемещение комментариев статусов документов в блок комментариев"""
    Document = apps.get_model('dcis', 'Document')
    DocumentMessage = apps.get_model('dcis', 'DocumentMessage')
    User = apps.get_model('core', 'User')
    for document in Document.objects.all():
        for document_status in document.documentstatus_set.all():
            user = document.user or document.period.user or User.objects.get(username='support@cbias.ru')
            status_part = f'Статус документа: {document_status.status.name}.'
            comment_part = document_status.comment if document_status.comment else ''
            dm = DocumentMessage.objects.create(
                comment=f'{status_part} {comment_part}',
                kind='status',
                user=user,
                document=document
            )
            dm.created_at = document_status.created_at
            dm.save(update_fields=('created_at',))


def empty_reverse(apps, schema_editor):
    """Пустая функция для отката миграции."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('dcis', '0041_remove_document_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentmessage',
            name='kind',
            field=models.CharField(choices=[('message', 'message'), ('status', 'status')], default='message', help_text='Тип сообщения', max_length=30),
        ),
        migrations.RunPython(move_document_status_comments, empty_reverse)
    ]
