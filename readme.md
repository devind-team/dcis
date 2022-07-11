# Проект сборов


[Документация проекта.](docs/README.md)


# Для разработчиков

Приложение состоит из двух сервисов:

* Django сервер, реализующий GraphQL API (папка `server`)
* SSR Nuxt клиент (папка `client`)

Для работы приложения должны быть запущены **оба сервиса**.

## IDE
Рекомендованной средой разработки является PyCharm.

Обязательные плагины:
* Vue.js
* Pug
* GraphQL

Рекомендованные плагины:
* GitToolBox
* Conventional Commit

## Настройка Django сервера (папка `server`)
Для работы сервиса обязательно необходимы следующие зависимости:

| Зависимость                                                  | Версия |
|--------------------------------------------------------------|--------|
| [Python](https://www.python.org/downloads/)                  | 3.10   |
| [Poetry](https://python-poetry.org/docs/#installation)       | latest |
| [PostgreSQL](https://www.postgresql.org/download/)           | latest |
| [Redis](https://redis.io/docs/getting-started/installation/) | latest |

Для Windows Redis официально не поддерживается,
поэтому необходимо или установить WSL, как это описано на 
[сайте Redis](https://redis.io/docs/getting-started/installation/install-redis-on-windows/),
или воспользоваться [неофициальном портом](https://github.com/tporadowski/redis/releases).

В исключительных сценариях, для преобразования docx в pdf может потребоваться установленный
[LibreOffice](https://www.libreoffice.org/).
Для запуска таких сценариев из Windows
рекомендуется запускать Django сервер в WSL с установленным LibreOffice.

Здесь и далее все команды
должны выполняться из папки `server`, для перехода необходимо выполнить команду:
```shell
cd server
```
Префикс `poetry run` для всех команд может быть опущен
при активированном виртуальном окружении в терминале.
Активация окружения описана в секции "Дополнительные настройки PyCharm".

После установки зависимостей необходимо:

1. Создать базу данных PostgreSQL.

Имя базы данных по умолчанию - `devind`.

2. Создать `.env` файл в папке `server`.  

Создать файл можно путем копирования файла `.env.example` с новым названием `.env`.

При необходимости в файле нужно поменять данные для подключения к базе данных:
* Имя базы данных (ключ `DB_APP_NAME`)
* Пользователь (ключ `DB_APP_USER`)
* Пароль (ключ `DB_APP_PASSWORD`)

На **Windows** также необходимо удалить из созданного файла все комментарии, начинающиеся с символа `#`.

3. Установить зависимости Python

Для установки зависимостей Python необходимо выполнить команду:  
```shell
poetry install
```

4. Убедиться в том, что Redis сервер запущен

На Linux это можно сделать следующей командой:
```shell
sudo service redis-server restart
```

На macOS необходимо выполнить следующую команду:
```shell
brew services start redis
```

На Windows необходимо зайти в диспетчер задач и запустить службу `Redis`,
если она остановлена.

5. Выполнить скрипт, заполняющий базу данных начальными данными

Сделать это можно следующей командой:
```shell
# Unix
poetry run python3 manage.py migrate
poetry run python3 manage.py fs
# Windows
poetry run python manage.py migrate
poetry run python manage.py fs
```

Далее сервис может быть запущен следующей командой:
```shell
# Unix
poetry run python3 manage.py runserver
# Windows
poetry run python manage.py runserver
```

### Дополнительные настройки PyCharm
Для удобной работы с сервисом из PyCharm необходимо:

1. Активировать Python окружение в терминале

Для активации окружения необходимо перейти `File`, `Settings`, `Project: dcis`, `Python interpreter`.
Далее необходимо нажать на кнопку с шестеренкой, далее кнопка `Add`.
В открывшемся диалоговом меню необходимо выбрать пункт `Poetry Environment`, далее `Existing Environment`.
Pycharm должен автоматически определить путь к окружению, созданному с помощью команды `poetry install`.
Далее необходимо нажать на кнопку `Ok` в обоих меню.

2. Настроить Django

Для настройки Django необходимо перейти `File`, `Settings`, `Languages & Frameworks`, `Django`.
Далее необходимо активировать пункт `Enanle Django Support`,
выбрать папку `server` в качестве `Django project root`,
а файл `server/deving/settings.py` в качестве `Settings`, затем нажать на кнопку `Ок`.

3. Настроить конфигурацию

Настройка конфигурации осуществляется в правом верхнем углу возле кнопки `Run`.
Необходимо выбрать или `Add Configuration...`, если ни одна конфигурация не создана,
или `Edit Configurations...`, если ранее были созданы конфигурации.
Далее необходимо нажать на кнопку `+` в левом верхнем углу,
выбрать `Django Server` из списка, ввести имя конфигурации (например, "server")
и нажать на кнопку `Ok`.

4. Подключить базу данных для работы из PyCharm

Подключение базы данных осуществляется в правом верхнем углу.
Необходимо нажать на кнопку `Database`, затем на кнопку `+`, далее выбрать `DataSource`, `PostgreSQL`.
В появившемся окне необходимо подтвердить установку драйвера, если PyCharm её предлагает, затем заполнить поля
в соответствии с данными для подключения из файла `.env` и нажать на кнопку `Ok`.

После описанных выше действий появляется возможность:
1. Запускать команды без префикса `poetry run`.
2. Пользоваться `Python Console` c настроенным и запущенным Django.
3. Запускать сервис путем нажатия кнопки `Run`.
4. Взаимодействовать с базой данных из PyCharm.

## Настройка Nuxt клиента (папка client)
Для работы сервиса необходимы следующие зависимости:

| Зависимость                                               | Версия     |
|-----------------------------------------------------------|------------|
| [Node.js](https://nodejs.org/en/)                         | latest LTS |
| [Yarn](https://classic.yarnpkg.com/lang/en/docs/install/) | latest     |

После установки зависимостей необходимо:

1. Создать `.env` файл в папке `client`.

Создать файл можно путем копирования файла `.env.example` с новым названием `.env`.

2. Установить зависимости Node.js.

Для установки зависимостей Node.js необходимо перейти в папку `client` и выполнить команду:  
```shell
yarn
```

3. Создать символическую ссылку между клиентом и сервером.

Для возможности выгрузки файлов необходимо создать символическую ссылку
на папку `server/storage` в папке `client/static`.

Для этого в Unix необходимо в корне проекта выполнить команду:
```shell
python3 init.py
```

В Windows необходимо открыть терминал от имени администратора
и в корне проекта выполнить команду:
```shell
python init.py
```

Далее сервис может быть запущен из папки `client` следующей командой:
```shell
yarn run dev
```

### Дополнительные настройки PyCharm
Для удобной работы с сервисом из PyCharm необходимо настроить конфигурацию.

Настройка конфигурации осуществляется в правом верхнем углу возле кнопки `Run`.
Необходимо выбрать или `Add Configuration...`, если ни одна конфигурация не создана,
или `Edit Configurations...`, если ранее были созданы конфигурации.
Далее необходимо нажать на кнопку `+` в левом верхнем углу и
выбрать `npm` из списка.
Затем необходимо ввести имя конфигурации (например, "client"),
выбрать в качестве файла `package.json` файла `client/package.json`,
а в качестве `Scripts` команду `dev`. В конце необходимо нажать на кнопку `Ок`.

После настройки конфигурации появляется возможность запускать сервис путем нажатия кнопки `Run`.

> Для запуска Node v18+ может потребоваться флаг `NODE_OPTIONS=--openssl-legacy-provider`.


# Для системных администраторов

## Минимальные требования к сервера

Системные требования сервера:
* ОС: любой дистрибутив Linux(Ubuntu, Debian и т. д.)
* Двухъядерный процессор с частотой 2 ГГц или лучше
* Оперативной памяти минимум 4 Гб
* 32 Гб свободного пространства на жестком диске

Кроме этого на сервере должны быть установлены следующие зависимости:

| Зависимость                                                                   |  Версия  |
|-------------------------------------------------------------------------------|:--------:|
| [PostgreSQL](https://www.postgresql.org/download/)                            |  latest  |
| [docker](https://docs.docker.com/engine/install/ubuntu)                       |  latest  |
| [docker-compose](https://docs.docker.com/compose/install/compose-desktop)     |  latest  |
| [Nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/) |  latest  |

## Развертка и настройка электронной образовательной среды

После установки всех зависомостей необходимо:
1. [Аутентифицироваться в реестре контейнеров](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry):
    ```shell
    docker login ghcr.io -u USERNAME -p TOKEN
    ```
2. Создать директорию для хранения файлов и конфигурационные файлы для развертывания элетронной образовательной среды:
   1. Создание директории:
        ```shell
        sudo mkdir /var/www/eleden/storage 
        ```
   2. Создать файл `.env` со следующим содержимом:
        ```env_file
        # Client settings
        # Data connection
        APP_NAME='Электронная образовательная среда'
        URL=https://example.ru
        API_URL=http://192.168.1.3:8000/graphql/
        API_URL_BROWSER=https://example.ru/graphql/
        WS_URL=wss://example.ru/graphql/
        CLIENT_ID=
        CLIENT_SECRET=
        # Settings for sentry
        SENTRY_CLIENT_DSN=
        TINYMCE_API=
        ASK=
        # Server settings
        SECRET_KEY=
        DEBUG=False
        # Application database data
        DB_APP_HOST=
        DB_APP_NAME=
        DB_APP_USER=
        DB_APP_PASSWORD=
        # Email settings
        EMAIL_HOST=
        EMAIL_HOST_USER=
        EMAIL_HOST_PASSWORD=
        EMAIL_HOST_SUPPORT=
        # Sentry integration
        SENTRY_DNS=
        # Notification service interation
        FCM_API_KEY=
        # Settings for celery
        REDIS_SERVER=redis
        # Data for celery
        BROKER_URL=redis://redis:6379
        BROKER_BACKEND=redis://redis:6379
        TASK_SERIALIZER=json
        RESULT_SERIALIZER=json
        ```
   3. Создать файл `docker-compose.yml` со следующим содержимом:
        ```yml
        version: '3.7'
        
        services:
          client:
            container_name: client
            image: ghcr.io/devind-team/eleden/eleden-client:latest
            command: yarn run nuxt start
            restart: always
            ports:
              - "3000:3000"
            env_file: .env
        
          api:
            container_name: api
            image: ghcr.io/devind-team/eleden/eleden-server:latest
            command: poetry run daphne -b 0.0.0.0 -p 8000 devind.asgi:application
            restart: always
            ports:
              - "8000:8000"
            env_file: .env
            volumes:
              - "/var/www/eleden/storage:/usr/src/app/storage"
        
          celery:
            container_name: celery
            image: ghcr.io/devind-team/eleden/eleden-server:latest
            command: poetry run celery -A devind worker -B -E -l INFO
            restart: always
            env_file: .env
            volumes:
              - "/var/www/eleden/storage:/usr/src/app/storage"
        
          redis:
            image: redis
            restart: always
        ```
3.  Создать и запустить докер контейнеры:
    > Команды `docker-compose` выполняюся в директории, где находится файл `docker-compose.yml`
    ```shell
    # Извлечение образа
    sudo docker-compose pull
    # Создание и запуск контейнеров
    sudo docker-compose up -d
    ```
4. Создать и настроить базу данных:
   1. Создание пользователя, базы данных и присвоение всех привилегий пользователю над базой данных:
    ```shell
    # Подключение к PostgreSQL
    sudo psql -U postgres
    ```
    ```PostgreSQL
    create user username with encrypted password 'user_password';
    create database database_name;
    grant all privileges on database database_name to username;
    grant connect on database database_name TO username;
    ```
    1. Изменить конфигурационный файл PostgreSQL(`/etc/postgresql/latest_version/main/`), добавив в него записи:
    ```
    host    database_name         username        ip_addres_docker_container/24           md5
    ```
    1. Перезапустить PostgreSQL
    ```shell
    sudo service postgresql restart
    ```
5. Наполнение базы данных начальными данными:
    ```shell
    # Создание таблиц в базе данных
    sudo docker-compose run api poetry run python manage.py migrate
    # Наполнение базы данных начальными данными
    sudo docker-compose run api poetry run python manage.py fs
    ```
6. Настройка `nginx`
   1. Создать файл в `/etc/nginx/sites-available` со следующим содержимом:
    ```nginx
    upstream channels-site {
        server localhost:8000;
    }
    
    server {
        listen 443 ssl http2;
        server_name site.ru www.site.ru;
    
        access_log /var/log/nginx/site.ru.access.log;
        error_log /var/log/nginx/site.ru.error.log;
    
        client_max_body_size 32m;
    
        #ssl on;
        ssl_certificate /etc/ssl/certificate/site.crt;
        ssl_certificate_key /etc/ssl/certificate/site.key;
    
        location /storage/ {
            alias /var/www/site/storage/;
        }
    
        location /graphql/ {
            proxy_pass http://channels-site;
    
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
    
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $server_name;
        }
    
        location / {
            proxy_pass http://localhost:3000;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    
    server {
        listen 80;
        server_name site.ru www.site.ru;
        return 301 https://$host$request_uri;
    }
    ```
   2. Создать символическую ссылку созданного файла в `/etc/nginx/sites-enabled`:
    ```shell
    ln -s /etc/nginx/sites-available/file_name.conf /etc/nginx/sites-enabled
    ```
   3. Перезапустить `nginx`
    ```
    sudo service nginx restart
    ```

## Генерация API сервера

В папке docs:
```shell
sphinx-apidoc -o . ..
make markdown # Для генерации md файлов
make html # Для генерации html файлов
```