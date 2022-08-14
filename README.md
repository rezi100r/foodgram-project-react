# Продуктовый помощник (дипломный проект)
![Foodgram project workflow Status](https://github.com/rezi100r/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=main&event=push)
## Описание:

Адрес сайта: http://orphan-practicum.webhop.me/
IP: 84.252.140.254
Доступ на сайт:
admin@admin.com/P@$$w0rd!
Доступ к админке
admin/P@$$w0rd!

### Проект "**Продуктовый помощник**" это онлайн-сервис на котором пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Варианты запуска проекта

### Запуск проекта в dev-режиме без контейнеров
```
python -m venv env
source env/bin/activate (env/Scripts/activate)
cd backend/
python -m pip install --upgrade pip
pip install -r requirements.txt
```
#### Наполнение env-файла:

С помощью команды ниже в папке будет создан .env-файл

```py
echo '''SECRET_KEY=super-key
DEBUG=True
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
''' > .env
```

#### Запуск проекта

```
python manage.py migrate
python manage.py createsuperuser
python manage.py load_tags
python manage.py load_ingredients
python manage.py runserver
```

### Запуск проект в контейнерах:

#### Наполнение env-файла для базы данных PostgreSQL:

С помощью команды ниже в папке будет создан .env-файл

```py
echo '''DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db 
DB_PORT=5432
SECRET_KEY=super-key
DEBUG=True
''' > .env
```
#### Сборка и запуск
```
cd foodgram-project-react/infra/
docker-compose up -d --build
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py load_tags
docker-compose exec backend python manage.py load_ingredients
```

## Автор

### Разработчик backend Егорченков Николай