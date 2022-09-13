"""Модуль с командой для применения фикстур."""
import time
from os import listdir
from os.path import exists, join

from django.core.management import call_command
from django.core.management.base import BaseCommand

from django.apps import apps


class Command(BaseCommand):
    """Команда применения фикстур проекта."""

    helps = 'Первоначальное развертывание проекта.'

    def add_arguments(self, parser) -> None:
        """Аргументы команды."""
        parser.add_argument(
            '--app',
            help='Указываем приложение для парсинга'
        )

    def app_fixtures(self, app: str, fixture_location: str) -> None:
        """Применение фикстуры."""
        if exists(fixture_location):
            self.stdout.write(f'  Приложение {app}:')
            for fixture in sorted(listdir(fixture_location)):
                self.stdout.write(f'    Модель {fixture[4:-5]}')
                call_command('loaddata', fixture)

    def handle(self, *args, **options) -> None:
        """Описание команды."""
        start_time = time.time()
        self.stdout.write('Инициализация проекта:')
        if options['app']:
            for app in apps.get_app_configs():
                if app.label == options['app']:
                    self.app_fixtures(app=app.label, fixture_location=join(app.path, 'fixtures'))
                else:
                    self.stdout.write(f'В приложении отсутствуют фикстуры {app.label}.')
        else:
            for app in apps.get_app_configs():
                self.app_fixtures(app=app.label, fixture_location=join(app.path, 'fixtures'))
        self.stdout.write(f'Развертывание проекта завершено за время: {str((time.time() - start_time) / 60)} минут')
