# PinkCode

PinkCode — это платформа для тренировки навыков программирования, создания и решения задач, а также соревнований между пользователями. Проект реализован на Django + DRF (бэкенд), Celery (асинхронное выполнение кода), PostgreSQL, Redis и фронтенде на HTML/CSS/JS.

![Архитектура PinkCode](https://raw.githubusercontent.com/yourusername/pinkcode/main/docs/architecture.png)

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