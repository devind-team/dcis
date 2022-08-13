"""Модуль с командой загрузки базы данных из боевого сервера."""

import os
import platform
import shutil
from contextlib import contextmanager
from datetime import datetime
from os import path, mkdir
from typing import Any

import paramiko
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from paramiko import AuthenticationException
from pytz import timezone


class Command(BaseCommand):
    """Команда загрузки базы данных из боевого сервера."""

    help = 'Загрузка базы данных из боевого сервера'

    tmp_dir = path.join(settings.BASE_DIR, 'storage', 'backup')
    remote_path_dir = f'/var/backups_databases/{settings.SSH_CONNECT["DB_NAME"]}/'
    now = datetime.now(timezone('Europe/Moscow'))

    @classmethod
    def create_backup(cls, options: dict[str, Any]) -> None:
        """Создание нового бэкапа на боевом сервере.
        :param options: словарь аргументов
        """

        cmd = f'pg_dump postgresql://postgres:1234@127.0.0.1:5432/{settings.SSH_CONNECT["DB_NAME"]} > ' \
              f'{cls.remote_path_dir}{settings.SSH_CONNECT["DB_NAME"]}' \
              f'_backup_{cls.now.strftime("%Y-%m-%d-%H:%M:%S")}.sql'
        with cls.connect(options) as ssh:
            ssh.exec_command(cmd)

    @classmethod
    def copy_backup(cls, options: dict[str, Any]) -> str:
        """Копирование бэкапа из боевого сервера.
        :param options: словарь аргументов
        :return: путь к скопированному бэкапу
        """
        with cls.connect(options) as ssh:
            sftp = ssh.open_sftp()
            files_list = sftp.listdir(cls.remote_path_dir)
            files_sort = sorted(files_list, reverse=True)
            file_name = files_sort[0]
            remote_path = path.join(cls.remote_path_dir, file_name)
            mkdir(cls.tmp_dir)
            local_path = path.join(cls.tmp_dir, file_name.replace(':', ''))
            sftp.get(remote_path, local_path)
            sftp.close()
        return local_path

    def delete_tables(self) -> None:
        """Удаление всех таблиц."""
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_schema, table_name FROM information_schema.tables "
                           "WHERE table_schema = 'public' ORDER BY table_schema, table_name")
            rows = cursor.fetchall()
            for row in rows:
                self.stdout.write(f'Удаление таблицы: {row[1]}')
                cursor.execute('drop table ' + row[1] + ' cascade')

    def apply_backup(self, local_path: str) -> None:
        """Применение бэкапа.
        :param local_path: путь к бэкапу
        """
        cmd = f"postgresql://{settings.DATABASES['default']['USER']}:" \
              f"{settings.DATABASES['default']['PASSWORD']}@" \
              f"{settings.DATABASES['default']['HOST']}:" \
              f"{settings.DATABASES['default']['PORT']}/" \
              f"{settings.DATABASES['default']['NAME']} < {local_path}"
        if platform.system() in ('Linux', 'Darwin'):
            os.system('psql ' + cmd)
        elif platform.system() == 'Windows':
            os.system('"C:\\Program Files\\PostgreSQL\\14\\bin\\psql.exe" ' + cmd)
        else:
            self.stdout.write('Данная команда не работает для вашей платформы. \n'
                              'Необходимо выполнить ручной экспорт данных: \n'
                              'psql postgresql://пользователь:пароль@хост:порт/имя БД'
                              ' < (путь к файлу) ')

    @staticmethod
    @contextmanager
    def connect(options: dict[str, Any]) -> paramiko.SSHClient:
        """Подключение по ssh.
        :param options: словарь аргументов
        :return: ssh клиент
        """

        ssh = paramiko.SSHClient()
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                settings.SSH_CONNECT['HOST'],
                port=settings.SSH_CONNECT['PORT'],
                username=options['username'] or settings.SSH_CONNECT['USERNAME'],
                password=options['password'] or settings.SSH_CONNECT['PASSWORD']
            )
            yield ssh
        finally:
            ssh.close()

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--username',
            help='Имя пользователя'
        )
        parser.add_argument(
            '-p',
            '--password',
            help='Пароль пользователя'
        )
        parser.add_argument(
            '-c',
            '--create_backup',
            action='store_true',
            help='Создавать ли новый бэкап'
        )

    def handle(self, *args, **options):
        try:
            if options['create_backup']:
                self.create_backup(options)
            local_path = self.copy_backup(options)
        except AuthenticationException:
            self.stdout.write('Невозможно подключиться по ssh. Проверьте правильность параметров.')
            return
        try:
            self.delete_tables()
            self.apply_backup(local_path)
        finally:
            shutil.rmtree(self.tmp_dir)
