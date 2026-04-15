# ПК-Майстерня (Iron Student)

Освітня платформа для навчання студентів збірки комп'ютерів.

## Запуск (Docker) — рекомендовано

```bash
# 1. Установить Docker Desktop
# 2. Запуск:
docker-compose up --build

# 3. Открыть в браузере:
http://localhost:8000

# Остановить:
docker-compose down
```

## Запуск (без Docker)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/despair33/iron-student.git
cd iron-student

# 2. Создать виртуальное окружение
python -m venv venv

# 3. Активировать (Windows)
venv\Scripts\activate

# 3. Активировать (Linux/Mac)
source venv/bin/activate

# 4. Установить зависимости
pip install -r backend/requirements.txt

# 5. Миграции (при первой установке)
cd backend
python manage.py migrate

# 6. Запустить сервер
python manage.py runserver 0.0.0.0:8000

# 7. Открыть в браузере:
http://127.0.0.1:8000

# Создать суперпользователя (для админки):
python manage.py createsuperuser
```

## API Endpoints

- `GET /api/can-play/` — проверка доступа к игре
- `POST /api/save-test/` — сохранение результатов теста
- `GET /api/progress/` — прогресс игрока

## Структура

```
backend/     - Django бэкенд
frontend/   - Для фронтенд-разработчика
Dockerfile   - Контейнер
docker-compose.yml
```

## Стек

- Django 6.0
- Django REST Framework
- SQLite
- HTML/CSS/JS (Vanilla)