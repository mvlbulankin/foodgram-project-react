![example workflow](https://github.com/mvlbulankin/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Проект Foodgram

### Описание 
Проект Foodgram, «Продуктовый помощник» - онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

----

### Стек

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

----

В API доступны следующие эндпоинты:

### Пользователи:
* ```http://127.0.0.1:8000/api/users/``` GET-запрос — Получить список пользователей.

* ```http://127.0.0.1:8000/api/users/``` POST-запрос — Создать пользователя.

* ```http://127.0.0.1:8000/api/auth/token/login/``` POST-запрос — Получить токен авторизации.

* ```http://127.0.0.1:8000/api/auth/token/logout/``` POST-запрос — Удалить токен авторизации.

* ```http://127.0.0.1:8000/api/users/{id}/``` GET-запрос — Профиль пользователя.

* ```http://127.0.0.1:8000/api/users/me/``` GET-запрос — Текущий пользователь.

* ```http://127.0.0.1:8000/api/users/set_password/``` POST-запрос — Изменить пароль.

### Подписки:

* ```http://127.0.0.1:8000/api/users/subscriptions/``` GET-запрос — Список пользователей, на которых подписан текущий пользователь. В выдачу добавляются рецепты.

* ```http://127.0.0.1:8000/api/users/{id}/subscribe/``` POST-запрос — Подписаться на пользователя.

* ```http://127.0.0.1:8000/api/users/{id}/subscribe/``` DELETE-запрос — Отписаться от пользователя.

### Теги:

* ```http://127.0.0.1:8000/api/tags/``` GET-запрос — Список тегов.

* ```http://127.0.0.1:8000/api/tags/{id}/``` GET-запрос — Получить тег.

### Рецепты:

* ```http://127.0.0.1:8000/api/recipes/``` GET-запрос — Список рецептов.

* ```http://127.0.0.1:8000/api/recipes/``` POST-запрос — Создать рецепт.

* ```http://127.0.0.1:8000/api/recipes/{id}/``` GET-запрос — Получить рецепт.

* ```http://127.0.0.1:8000/api/recipes/{id}/``` PATCH-запрос — Обновить рецепт.

* ```http://127.0.0.1:8000/api/recipes/{id}/``` DELETE-запрос — Удалить рецепт.

### Ингридиенты:

* ```http://127.0.0.1:8000/api/ingredients/``` GET-запрос — Список ингридиентов.

* ```http://127.0.0.1:8000/api/ingredients/{id}/``` GET-запрос — Получить ингридиент.

### Избранное:

* ```http://127.0.0.1:8000/api/recipes/{id}/favorite/``` POST-запрос — Добавить рецепт в избранное.

* ```http://127.0.0.1:8000/api/recipes/{id}/favorite/``` DELETE-запрос — Удалить рецепт из избранного.

### Список покупок:

* ```http://127.0.0.1:8000/api/recipes/download_shopping_cart/``` GET-запрос — Скачать список покупок.

* ```http://127.0.0.1:8000/api/recipes/{id}/shopping_cart/``` POST-запрос — Добавить рецепт в список покупок.

* ```http://127.0.0.1:8000/api/recipes/{id}/shopping_cart/``` DELETE-запрос — Удалить рецепт из списка покупок.

----

### Как запустить проект:

Клонируйте репозиторий и переходите в него в командной строке:

```
git clone git@github.com:mvlbulankin/foodgram-project-react.git
```

```
cd infra
```

Запустите контейнеры:

```
docker compose up -d
```

Выполните миграции:

```
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
```

Создайте суперпользователя:

```
docker compose exec backend python manage.py createsuperuser
```

Соберите статику:

```
docker compose exec backend python manage.py collectstatic --no-input
```

Импортируйте данные из csv-файлов в базу данных:

```
docker compose exec backend python manage.py load_data_csv --use_default_dataset
```

Зайдите на http://localhost/admin/ и убедитесь, 
что страница отображается полностью и статика подгрузилась:

----

### Автор проекта:

**Михаил Буланкин**
