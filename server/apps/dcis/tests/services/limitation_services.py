"""Тесты модуля, отвечающего за работу с ограничениями."""
import json
from collections import Counter
from os import listdir, remove
from os.path import isfile, join
from unittest.mock import patch

from devind_dictionaries.models import Organization
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase, override_settings

from apps.core.models import User
from apps.dcis.helpers.limitation_formula_cache import LimitationFormulaContainerCache
from apps.dcis.models import Limitation, Period, Project, Sheet
from apps.dcis.services.limitation_services import (
    add_limitation,
    add_limitations_from_file,
    change_limitation,
    delete_limitation,
    unload_limitations_in_file, update_limitations_from_file,
)
from apps.dcis.tests.tests_helpers import create_in_memory_file


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class LimitationTestCase(TestCase):
    """Тестирование ограничений."""

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.superuser = User.objects.create(username='superuser', email='superuser@gmain.com', is_superuser=True)

        self.organization_content_type = ContentType.objects.get_for_model(Organization)
        self.project = Project.objects.create(content_type=self.organization_content_type)

        self.add_file_period = Period.objects.create(project=self.project)
        self.add_file_period_form1 = Sheet.objects.create(name='Форма1', period=self.add_file_period)
        self.add_file_period_form2 = Sheet.objects.create(name='Форма2', period=self.add_file_period)

        self.update_file_period = Period.objects.create(project=self.project)
        self.update_file_period_form1 = Sheet.objects.create(name='Форма1', period=self.update_file_period)
        self.update_file_period_form2 = Sheet.objects.create(name='Форма2', period=self.update_file_period)
        self.update_file_period_container_cache = LimitationFormulaContainerCache.get(self.update_file_period)
        self.update_file_period_limitation = Limitation.objects.create(
            index=1,
            formula='Форма1!A1 > Форма2!A1',
            error_message='update_file_period_limitation',
            sheet=self.update_file_period_form1,
        )

        self.add_period = Period.objects.create(project=self.project)
        self.add_period_form1 = Sheet.objects.create(name='Форма1', period=self.add_period)
        self.add_period_form2 = Sheet.objects.create(name='Форма2', period=self.add_period)
        self.add_period_container_cache = LimitationFormulaContainerCache.get(self.add_period)
        self.add_period_limitation = Limitation.objects.create(
            index=1,
            formula='Форма1!A1 > Форма2!A1',
            error_message='add_period_limitation',
            sheet=self.add_period_form1,
        )
        self.add_period_container_cache.add_limitation_formula(self.add_period_limitation).save()

        self.change_period = Period.objects.create(project=self.project)
        self.change_period_form1 = Sheet.objects.create(name='Форма1', period=self.change_period)
        self.change_period_form2 = Sheet.objects.create(name='Форма2', period=self.change_period)
        self.change_period_container_cache = LimitationFormulaContainerCache.get(self.change_period)
        self.change_period_limitation1 = Limitation.objects.create(
            index=1,
            formula='Форма1!A1 > Форма2!A1',
            error_message='change_period_limitation1',
            sheet=self.change_period_form1,
        )
        self.change_period_container_cache.add_limitation_formula(self.change_period_limitation1)
        self.change_period_limitation2 = Limitation.objects.create(
            index=2,
            formula='Форма2!B1 > Форма1!A1',
            error_message='change_period_limitation2',
            sheet=self.change_period_form2,
        )
        self.change_period_container_cache.add_limitation_formula(self.change_period_limitation2)
        self.change_period_container_cache.save()

        self.delete_period = Period.objects.create(project=self.project)
        self.delete_period_form1 = Sheet.objects.create(name='Форма1', period=self.delete_period)
        self.delete_period_form2 = Sheet.objects.create(name='Форма2', period=self.delete_period)
        self.delete_period_container_cache = LimitationFormulaContainerCache.get(self.delete_period)
        self.delete_period_limitation1 = Limitation.objects.create(
            index=1,
            formula='Форма1!A1 > Форма2!A1',
            error_message='delete_period_limitation1',
            sheet=self.delete_period_form1,
        )
        self.delete_period_container_cache.add_limitation_formula(self.delete_period_limitation1)
        self.delete_period_limitation2 = Limitation.objects.create(
            index=2,
            formula='Форма1!A1 < Форма2!B1',
            error_message='delete_period_limitation2',
            sheet=self.delete_period_form1,
        )
        self.delete_period_container_cache.add_limitation_formula(self.delete_period_limitation2)
        self.delete_period_limitation3 = Limitation.objects.create(
            index=3,
            formula='Форма2!C1 > Форма1!A1',
            error_message='delete_period_limitation3',
            sheet=self.delete_period_form2,
        )
        self.delete_period_container_cache.add_limitation_formula(self.delete_period_limitation3)
        self.delete_period_container_cache.save()

    def test_add_limitations_from_file_with_errors(self) -> None:
        """Тестирование функции `add_limitations_from` c ошибками."""
        self._test_add_limitations_from_file_with_error(
            'test_add_limitations_from_file_wrong_json.json', [
                'Не удалось разобрать json файл',
                'Expecting property name enclosed in double quotes',
            ]
        )
        self._test_add_limitations_from_file_with_error(
            'test_add_limitations_from_file_not_list.json', [
                'json файл не содержит массив на верхнем уровне'
            ]
        )
        self._test_add_limitations_from_file_with_error(
            'test_add_limitations_from_file_not_dict.json', [
                'Ограничение по номеру 2 не является объектом'
            ]
        )
        self._test_add_limitations_from_file_with_error(
            'test_add_limitations_from_file_wrong_keys.json', [
                'Ключи ограничения по номеру 2 должны совпадать со списком ["form", "check", "message"]'
            ]
        )
        self._test_add_limitations_from_file_with_error(
            'test_add_limitations_from_file_wrong_sheet.json', [
                'Не найдена форма "Форма3" для ограничения по номеру 2'
            ]
        )

    def test_add_limitations_from_file(self) -> None:
        """Тестирование функции `add_limitations_from` без ошибок."""
        limitations = add_limitations_from_file(
            self.add_file_period,
            create_in_memory_file('test_add_update_limitations_from_file.json')
        )
        self._test_add_update_limitations_from_file(limitations, self.add_file_period)

    def test_update_limitations_from_file(self) -> None:
        """Тестирование функции `update_limitations_from_file`."""
        with patch.object(
            self.superuser, 'has_perm', lambda perm: perm != 'dcis.change_period'
        ), self.assertRaises(PermissionDenied) as error:
            update_limitations_from_file(
                self.superuser,
                self.update_file_period,
                create_in_memory_file('test_add_update_limitations_from_file.json')
            )
        self.assertEqual('Недостаточно прав для изменения ограничений периода.', str(error.exception))
        limitations = update_limitations_from_file(
            self.superuser,
            self.update_file_period,
            create_in_memory_file('test_add_update_limitations_from_file.json')
        )
        self.assertFalse(Limitation.objects.filter(id=self.update_file_period_limitation.id).exists())
        self._test_add_update_limitations_from_file(limitations, self.update_file_period)

    def test_add_limitation(self) -> None:
        """Тестирование функции `add_limitation`."""
        add_data = {
            'formula': 'Форма2!B1 > Форма1!A1',
            'error_message': 'add_limitation',
            'sheet_id': self.add_period_form2.id,
        }
        with patch.object(
            self.superuser, 'has_perm', lambda perm: perm != 'dcis.change_period'
        ), self.assertRaises(PermissionDenied) as error:
            add_limitation(self.superuser, **add_data)
        self.assertEqual('Недостаточно прав для изменения ограничений периода.', str(error.exception))
        limitation = add_limitation(self.superuser, **add_data)
        self.assertEqual(limitation.index, 2)
        for k, v in add_data.items():
            self.assertEqual(v, getattr(limitation, k))
        self.add_period_container_cache = LimitationFormulaContainerCache.get(self.add_period)
        self.assertEqual(
            {
                'A1': Counter(['Форма1!A1', 'Форма2!A1']),
                'A2': Counter(['Форма1!A1', 'Форма2!B1']),
            },
            self.add_period_container_cache.dependency_cache.dependency,
        )
        self.assertEqual(
            {'Форма1!A1': ['A1', 'A2'], 'Форма2!A1': ['A1'], 'Форма2!B1': ['A2']},
            self.add_period_container_cache.dependency_cache.inversion,
        )

    def test_change_limitation(self) -> None:
        """Тестирование функции `change_limitation`."""
        change_data = {
            'formula': 'Форма1!A1 >= Форма2!B1 + Форма2!C1',
            'error_message': 'change_period_limitation2_changed',
            'sheet_id': self.change_period_form1.id,
        }
        with patch.object(
            self.superuser, 'has_perm', lambda perm: perm != 'dcis.change_period'
        ), self.assertRaises(PermissionDenied) as error:
            change_limitation(self.superuser, self.change_period_limitation2, **change_data)
        self.assertEqual('Недостаточно прав для изменения ограничений периода.', str(error.exception))
        limitation = change_limitation(self.superuser, self.change_period_limitation2, **change_data)
        self.assertEqual(self.change_period_limitation2, limitation)
        self.change_period_limitation2.refresh_from_db()
        for k, v in change_data.items():
            self.assertEqual(v, getattr(self.change_period_limitation2, k))
        self.change_period_container_cache = LimitationFormulaContainerCache.get(self.change_period)
        self.assertEqual(
            {
                'A1': Counter(['Форма1!A1', 'Форма2!A1']),
                'A2': Counter(['Форма1!A1', 'Форма2!B1', 'Форма2!C1']),
            },
            self.change_period_container_cache.dependency_cache.dependency,
        )
        self.assertEqual(
            {'Форма1!A1': ['A1', 'A2'], 'Форма2!A1': ['A1'], 'Форма2!B1': ['A2'], 'Форма2!C1': ['A2']},
            self.change_period_container_cache.dependency_cache.inversion,
        )

    def test_delete_limitation(self) -> None:
        """Тестирование функции `delete_limitation`."""
        expected_delete_id = self.delete_period_limitation2.id
        with patch.object(
            self.superuser, 'has_perm', lambda perm: perm != 'dcis.change_period'
        ), self.assertRaises(PermissionDenied) as error:
            delete_limitation(self.superuser, self.delete_period_limitation2)
        self.assertEqual('Недостаточно прав для изменения ограничений периода.', str(error.exception))
        actual_delete_id = delete_limitation(self.superuser, self.delete_period_limitation2)
        self.assertEqual(expected_delete_id, actual_delete_id)
        limitations = Limitation.objects.filter(sheet__period=self.delete_period)
        self.assertEqual(
            {self.delete_period_limitation1, self.delete_period_limitation3},
            set(limitations)
        )
        self.delete_period_limitation3.refresh_from_db()
        self.assertEqual(2, self.delete_period_limitation3.index)
        self.delete_period_container_cache = LimitationFormulaContainerCache.get(self.delete_period)
        self.assertEqual(
            {
                'A1': Counter(['Форма1!A1', 'Форма2!A1']),
                'A2': Counter(['Форма2!C1', 'Форма1!A1']),
            },
            self.delete_period_container_cache.dependency_cache.dependency,
        )
        self.assertEqual(
            {'Форма1!A1': ['A1', 'A2'], 'Форма2!A1': ['A1'], 'Форма2!C1': ['A2']},
            self.delete_period_container_cache.dependency_cache.inversion,
        )

    def _test_add_limitations_from_file_with_error(self, file_path: str, messages: list[str]) -> None:
        """Тестирование функции `add_limitations_from` c ошибкой."""
        with self.assertRaises(ValidationError) as error:
            add_limitations_from_file(
                self.add_file_period,
                create_in_memory_file(file_path)
            )
        self.assertEqual({'limitations_file': list(map(ValidationError, messages))}, error.exception.error_dict)

    def _test_add_update_limitations_from_file(self, limitations: list[Limitation], period: Period) -> None:
        """Тестирование функции `add_limitations_from_file` или `update_limitations_from_file`."""
        self.assertEqual(
            set(Limitation.objects.filter(sheet__period=period)),
            set(limitations)
        )
        limitation_container_cache = LimitationFormulaContainerCache.get(period)
        self.assertEqual(
            {
                'A1': Counter(['Форма1!A1', 'Форма2!A1']),
                'A2': Counter(['Форма1!A2', 'Форма2!A2'])
            },
            limitation_container_cache.dependency_cache.dependency
        )
        self.assertEqual(
            {
                'Форма1!A1': ['A1'],
                'Форма2!A1': ['A1'],
                'Форма1!A2': ['A2'],
                'Форма2!A2': ['A2'],
            },
            limitation_container_cache.dependency_cache.inversion
        )

    def test_unload_limitations_in_file(self):
        """Тестирование функции `unload_limitations_in_file`."""
        result = unload_limitations_in_file(self.superuser, self.update_file_period)

        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith('.json'))

        with open(join(settings.BASE_DIR, result)) as file:
            data = json.load(file)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def tearDown(self):
        """Remove the temporary files created during the test."""
        temp_dir = join(settings.STATICFILES_DIRS[1], 'temp_files')
        for file in listdir(temp_dir):
            file_path = join(temp_dir, file)
            if isfile(file_path):
                remove(file_path)
