FROM python:3.14-slim

WORKDIR /app

# Установка зависимостей
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Копирование проекта
COPY backend/ .
COPY templates/ ./templates/
COPY static/ ./static/

# Запуск
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]