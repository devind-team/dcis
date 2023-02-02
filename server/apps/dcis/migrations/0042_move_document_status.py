from django.db import migrations, models


def move_document_status_comments(apps, schema_editor):
    """Перемещение комментариев статусов документов в блок комментариев"""
    Document = apps.get_model('dcis', 'Document')
    DocumentMessage = apps.get_model('dcis', 'DocumentMessage')
    User = apps.get_model('core', 'User')
    for document in Document.objects.all():
        if document.last_status:
            user = document.user or document.period.user or User.objects.get(username='support@cbias.ru')
            status_part = f'Статус документа: {document.last_status.status.name}.'
            comment_part = document.last_status.comment if document.last_status.comment else ''
            DocumentMessage.objects.create(
                comment=f'{status_part} {comment_part}',
                kind='status',
                created_at=document.last_status.created_at,
                user=user,
                document=document
            )


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
