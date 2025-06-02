# PinkCode

PinkCode — это платформа для тренировки навыков программирования, создания и решения задач, а также соревнований между пользователями. Проект реализован на Django + DRF (бэкенд), Celery (асинхронное выполнение кода), PostgreSQL, Redis и фронтенде на HTML/CSS/JS.


## Возможности

- Регистрация и аутентификация пользователей (JWT)
- Просмотр, создание и решение задач по программированию (Python, SQL)
- Загрузка и управление тест-кейсами
- Асинхронная проверка решений через Celery
- Рейтинг пользователей и задач (лайки/дизлайки)
- Топ пользователей и личный профиль
- Админ-панель Django для управления сущностями

## Архитектура

- **Frontend**: HTML, CSS, JS, Bootstrap, Nginx (Docker)
- **Backend**: Django, Django REST Framework, Celery, Redis, PostgreSQL
- **Асинхронная обработка**: Celery worker и Celery beat для задач проверки решений
- **API**: RESTful, JWT-аутентификация

## Быстрый старт

### 1. Клонируйте репозиторий

```sh
git clone https://github.com/yourusername/pinkcode.git
cd pinkcode
```

### 2. Запуск через Docker Compose

```sh
docker-compose up --build
```

- Бэкенд: http://localhost:8000
- Фронтенд: http://localhost:3001

### 3. Миграции и суперпользователь

```sh
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 4. Открыть платформу

- Перейдите на [http://localhost:3001](http://localhost:3001) для работы с платформой.
- Админка: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Структура проекта

```
core/
  ├── auth                 # Пользователи и аутентификация
  ├── main                 # Основная логика задач, тест-кейсов, рейтинга
  ├── code_interpreter     # Проверка решений и Celery-задачи
  ├── users                # Профили и топ пользователей
  ├── authentication       # Пользовательские разрешения и сериализаторы  
  └── utils                # Утилиты
frontend/
  ├── *.html               # Страницы интерфейса
  ├── scripts/             # JS-скрипты
  ├── styles/              # CSS-стили
  └── static/              # Статика
```

## Переменные окружения

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` — настройки БД
- `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND` — настройки брокера Celery