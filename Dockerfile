FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем весь проект
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY db.sqlite3 ./ 2>/dev/null || true

# Создаем папки для staticfiles и media
RUN mkdir -p /app/staticfiles

# Запуск
EXPOSE 8000
CMD ["sh", "-c", "python backend/manage.py migrate && python backend/manage.py collectstatic --noinput && python backend/manage.py runserver 0.0.0.0:8000"]