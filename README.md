# Продуктовый помощник (дипломный проект)

## Описание:

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
### Наполнение env-файла:

С помощью команды ниже в папке будет создан .env-файл

```py
echo '''SECRET_KEY=super-key
DEBUG=1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
''' > .env
```

### Запуск проекта

```
python manage.py migrate
python manage.py createsuperuser
python manage.py load_tags
python manage.py load_ingredients
python manage.py runserver
```