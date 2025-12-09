# Telegram Bot Template

Шаблон для разработки Телеграм Ботов с админ панелью django, используя Django ORM

## Django

Проект: `web/`  
Настройки: `web/core/settings.py`  
manage.py: `web/manage.py`

Директория для медиа: `web/media` (При создании новых моделей нужно прописывать `upload_to='web/media/...'` т.к. nginx
берет медиа оттуда)

В проекте используется только одно приложение panel: `web/panel`  
Соответственно:  
Все модели лежат в `web/panel/models.py`  
Настройка Админ-панели: `web/panel/admin.py`

Для корректной работы важно запускать manage.py из корневой директории проекта ```python web/manage.py ...```

## Telegram Bot

Используется дефолтный aiogram v3

Проект: `bot/`  
Главный файл: `bot/main.py`  
Handlers: `bot/core/handlers/` (При создании новых нужно импортировать и подключить роутер оттуда в
`bot/core/handlers/__init__.py`)  
Middlewares: `bot/core/middlewares.py` (сейчас там один middleware, который прокидывает модель юзера)  
Filters: `bot/core/filters.py` (сейчас там один filter для отсеивания всех чатов кроме личных)  
Keyboards: `bot/core/keyboards.py`  
FSM States: `bot/core/states.py`

Для корректной работы важно запускать main.py из корневой директории проекта ```python bot/main.py```

## Celery

В данном шаблоне используется для рассылок с помощью `requests`

Файл настройки: `web/core/celery.py`  
Файл с тасками: `web/panel/tasks.py`

Для корректной работы важно запускать celery из корневой директории проекта
`celery -A web.core worker --loglevel=info --pool=solo`

## Celery Beat

Используется для выполнения периодических задач в фоне.

Для корректной работы важно запускать celery beat из корневой директории проекта
`celery -A web.core beat --loglevel=info`

## Переменные окружения

Должны храниться в корневой директории проекта, в `.env` файле
Он должен содержать следующее

```dotenv
COMPOSE_PROJECT_NAME=... # Любое имя проекта. Подтягивается в Docker Compose
BOT_TOKEN=... # Токен бота

DEBUG=True/False # Debug mode для Django (Обязательно ставить False, при деплое)
TIMEZONE=Europe/Moscow # Часовой пояс для Django и Celery

DJANGO_ALLOWED_HOSTS=["localhost"]
DJANGO_CSRF_TRUSTED_ORIGINS=["http://localhost"]

# Настройки postgres
DB_NAME=db # Название БД
DB_USER=user # Логин БД
DB_PASSWORD=password # Пароль БД
DB_HOST=postgres # при DEBUG=False подставляется localhost
DB_PORT=5432 # порт в docker compose не прописан, поэтому оставляем дефолтный

# Настройки redis
REDIS_HOST=redis # при DEBUG=False подставляется localhost
REDIS_PORT=6379 # порт в docker compose не прописан, поэтому оставляем дефолтный
```

`.env` файл проверяется в `config.py`, откуда они все и тянутся в django, celery, telegram bot.

## Docker Compose

В данном проекте существует два docker compose файла.  
`.docker/docker-compose.dev.yaml` - postgres, redis запускаются на localhost (При запуске важно ставить DEBUG=True)  
`.docker/docker-compose.prod.yaml` - postgres, redis, celery, telegram_bot, nginx, django (При запуске важно ставить
DEBUG=False)

### Nginx

Используется как reverse proxy для django   
DockerFile: `.docker/nginx/DockerFile`  
Файл конфигурации: `.docker/nginx/nginx.conf`

### Django, Telegram Bot, Celery (Основанные на python образе)

DockerFile: `.docker/default/DockerFile`

### Postgres, Redis

Настраиваются в docker compose files

### Shell Scripts

Поскольку docker compose файла два и при этом нужно тянуть .env файл при запуске любого из них получается довольно
длинная строка  
`sudo docker compose -f .docker/docker-compose.[dev/prod].yaml --env-file=.env up --build`

Для удобства созданы два shell scripts (Соответственно не работают на Windows):

`sh/dev/compose.sh`

```shell
#!/bin/bash
sudo docker compose -f .docker/docker-compose.dev.yaml --env-file=.env "$@"
```

и
`sh/prod/compose.sh`

```shell
#!/bin/bash
sudo docker compose -f .docker/docker-compose.prod.yaml --env-file=.env "$@"
```

Эти команды упрощают нам жизнь. Теперь для любой команды docker compose достаточно написать  
`sh/[dev/prod]/compose.sh [up/stop/build/...]`

## Deploy (подойдет и для локальной развертки)

1. Создаем (или копируем с .env.example) и заполняем .env файл (с DEBUG=False)
2. Собираем и запускаем композицию контейнеров ```sh/prod/compose.sh up --build -d```
   автоматически)
3. Создаем суперюзера для django admin ```sh/prod/compose.sh exec web python web/manage.py createsuperuser```

Миграции накатываются автоматически.
Админ-панель запустится на 80 порту

Чтобы обновить проект, достаточно:

```shell
sh/prod/compose.sh stop
git pull
sh/prod/compose.sh up
```

