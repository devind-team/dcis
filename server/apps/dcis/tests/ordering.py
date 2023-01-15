"""Тестирование модуля сортировок."""

from datetime import timedelta

import graphene
from devind_dictionaries.models import Organization
from devind_helpers.utils import gid2int
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import Document, Period, Project, Status
from apps.dcis.ordering import DocumentOrderedDjangoFilterConnectionField
from apps.dcis.schema.types import DocumentType


class DocumentOrderedDjangoFilterConnectionFieldTestCase(TestCase):
    """Тестирование класса `DocumentOrderedDjangoFilterConnectionField`."""

    class Query(graphene.ObjectType):
        documents = DocumentOrderedDjangoFilterConnectionField(DocumentType)

    schema = graphene.Schema(query=Query)

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.user = User.objects.create(username='user', email='user@gmail.com')
        self.organization_content_type = ContentType.objects.get_for_model(Organization)

        self.project = Project.objects.create(content_type=self.organization_content_type)
        self.period = Period.objects.create(project=self.project)
        self.documents: list[Document] = []
        self.organizations = [
            Organization.objects.create(name=f'organization{i}', attributes='') for i in range(6, 0, -1)
        ]
        self.statuses: list[Status] = [Status.objects.create(name=f'status{i}') for i in range(1, 3)]
        for i, organization in enumerate(self.organizations):
            self.documents.append(Document.objects.create(
                period=self.period,
                object_id=organization.id,
                object_name=organization.name,
            ))
            self.documents[-1].documentstatus_set.create(
                comment=f'comment{i}',
                status=self.statuses[0] if i > 2 else self.statuses[1],
                user=self.user,
            )
            self.documents[-1].last_status.created_at += timedelta(days=6 - i) if i > 2 else timedelta(days=i)
            self.documents[-1].last_status.save(update_fields=('created_at',))

    def test_division_ordering(self) -> None:
        """Тестирование сортировки по дивизиону."""
        result = self.schema.execute(self._get_query('["division"]'))
        document_ids = [gid2int(d['node']['id']) for d in result.data['documents']['edges']]
        self.assertEqual(
            [d.id for d in sorted(self.documents, key=lambda d: [d.object_name + str(d.object_id)])],
            document_ids,
        )

    def test_last_status_ordering(self) -> None:
        """Тестирование сортировки по последнему статусу."""
        result = self.schema.execute(self._get_query('["lastStatus"]'))
        document_ids = [gid2int(d['node']['id']) for d in result.data['documents']['edges']]
        self.assertEqual(
            [d.id for d in sorted(
                self.documents,
                key=lambda d: [d.last_status.status.name + str(d.last_status.created_at) + d.last_status.comment]
            )],
            document_ids,
        )

    @staticmethod
    def _get_query(order_by: str) -> str:
        return """query {
            documents(orderBy: %s) {
                edges {
                    node {
                        id
                    }
                }
            }
        }""" % order_by
