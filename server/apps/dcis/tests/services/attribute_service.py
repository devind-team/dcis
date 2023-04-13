"""Тесты модуля, отвечающего за работу с атребутами."""
import json
from io import BytesIO
from os import listdir, remove
from os.path import isfile, join
from unittest.mock import MagicMock, patch

from devind_dictionaries.models import Organization
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.core.models import User
from apps.dcis.models import (
    Attribute,
    Period,
    Project,
)
from apps.dcis.permissions import can_change_period_attributes
from apps.dcis.services.attribute_services import (
    change_attribute, create_attribute, unload_attributes_in_file,
    upload_attributes_from_file,
)


class AttributeTestCase(TestCase):
    """Тестирование агрегации."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""

        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.organization_content_type = ContentType.objects.get_for_model(Organization)
        self.project = Project.objects.create(content_type=self.organization_content_type)

        self.period = Period.objects.create(project=self.project)

        self.attribute1 = Attribute.objects.create(
            name='Attribute 1',
            placeholder='Placeholder 1',
            key='key1',
            kind='string',
            default='',
            mutable=True,
            period=self.period
        )

        self.attribute2 = Attribute.objects.create(
            name='Attribute 2',
            placeholder='Placeholder 2',
            key='key2',
            kind='boolean',
            default=False,
            mutable=False,
            period=self.period
        )

    def test_create_attributes(self):
        """Test creating attributes."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(
                PermissionDenied,
                can_change_period_attributes,
                self.superuser,
                self.period
            )
        self.assertEqual(
            create_attribute(
                user=self.superuser,
                period=self.period,
                name='Attribute 3',
                placeholder='Placeholder 3',
                key='key3',
                kind='string',
                default='7',
                mutable=True
            ),
            Attribute.objects.get(name='Attribute 3')
        )

    def test_change_attributes(self):
        """Test change attributes."""
        with patch.object(
            self.superuser,
            'has_perm',
            new=lambda perm: perm not in ('dcis.change_period', 'dcis.add_project', 'dcis.add_period')
        ):
            self.assertRaises(
                PermissionDenied,
                can_change_period_attributes,
                self.superuser,
                self.period
            )
        self.assertEqual(
            change_attribute(
                user=self.superuser,
                attribute=self.attribute1,
                name='Attribute 3',
                placeholder='Placeholder 3',
                key='key3',
                kind='string',
                default='7',
                mutable=True,
            ),
            Attribute.objects.get(name='Attribute 3')
        )

    def test_upload_attributes_from_file(self):
        """Тестирование функции `upload_attributes_in_file`."""
        attributes = [
            {
                'name': 'Attribute 3',
                'placeholder': 'Placeholder 3',
                'key': 'key3',
                'kind': 'string',
                'default': '',
                'mutable': True
            },
            {
                'name': 'Attribute 4',
                'placeholder': 'Placeholder 4',
                'key': 'key4',
                'kind': 'boolean',
                'default': 'False',
                'mutable': False
            }
        ]
        json_data = BytesIO(json.dumps(attributes).encode())
        result = upload_attributes_from_file(self.superuser, self.period, json_data)

        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(attr, Attribute) for attr in result))

        self.assertEqual(Attribute.objects.count(), 2)
        self.assertEqual(Attribute.objects.filter(period=self.period).count(), 2)

        attribute1 = Attribute.objects.get(key='key3')
        self.assertEqual(attribute1.name, 'Attribute 3')
        self.assertEqual(attribute1.placeholder, 'Placeholder 3')
        self.assertEqual(attribute1.kind, 'string')
        self.assertEqual(attribute1.default, '')
        self.assertTrue(attribute1.mutable)

        attribute2 = Attribute.objects.get(key='key4')
        self.assertEqual(attribute2.name, 'Attribute 4')
        self.assertEqual(attribute2.placeholder, 'Placeholder 4')
        self.assertEqual(attribute2.kind, 'boolean')
        self.assertTrue(attribute2.default, False)
        self.assertFalse(attribute2.mutable)

    def test_upload_attributes_in_file(self):
        """Тестирование функции `unload_attributes_in_file`."""
        get_host = MagicMock(return_value='http://testserver')
        result = unload_attributes_in_file(self.superuser, get_host, self.period)

        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith('.json'))

        with open(join(settings.BASE_DIR, result)) as file:
            data = json.load(file)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        get_host.assert_called_once_with(None)

    def tearDown(self):
        """Remove the temporary files created during the test."""
        temp_dir = join(settings.STATICFILES_DIRS[1], 'temp_files')
        for file in listdir(temp_dir):
            file_path = join(temp_dir, file)
            if isfile(file_path):
                remove(file_path)
