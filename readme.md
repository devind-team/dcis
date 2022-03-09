# Devind Launcher

Стартовый проект для установки

## Для разработчиков

Создание символической ссылки между клиентом и сервером
```shell script
ln -s ./server/storage  ./client/static/storage
```

Установка cryptography для MacOS
```shell script
env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" pip install cryptography
```
1.Открыть термнал,перейти в папку PyCharmProjects.

2.Из папки проектов прописать команду git clone <HTTPS ссылка проекта с гитлаба>.

3.После развертки проекта далее идет настройка виртуального окружения.

В верхнем правом углу клик по кнопке 'Debug Configuration' (рядом кнопка 'run'),
затем Edit Configurations, Add New Configuration:
1)Выбираем npm, затем dev.По умолчанию указываем путь к файлу package.json. Далее в
строке scripts указываем :dev и нажимаем ОК.
2)В левом верхнем углу на панели выбираем File, Settings.
Ищем строку с Django и нажинаем на неё.Далее заполняем поля:
Django project root: <путь к серверу>, settings: <settings.py>).
После установок перезагружаем PyCharm.

4.Добавление БД.
В правом углу открыть панель Database,кнопка new(+), Data Source , PostgreSQL.
Далее заполянем поля:
User: postgres
Password: 1234
Database: пустое поле
После заполнения полей жмем Test Connection и сохраняем.
5. Установка и заполнение
```shell
  cd client  && yarn 
  cd server && python manage.py migrate && python manage.py fs,
   python manage.py fs --app pages
   python manage.py fs -- app eleden ,
   python manage.py parse_plx
   # user admin
   # password 12345678
```
6. Точечное обновление
```shell
python manage.py update_seed -m core.Setting -f 001.core/003.Setting.json
```
7. 