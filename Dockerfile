FROM python:3.14-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем весь проект
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY init_admin.py /app/init_admin.py
RUN chmod +x /app/init_admin.py

# Создаем папку для staticfiles
RUN mkdir -p /app/staticfiles

# Запуск с инициализацией
EXPOSE 8000
CMD ["sh", "-c", "python backend/manage.py migrate && python backend/manage.py collectstatic --noinput && python /app/init_admin.py && python backend/manage.py runserver 0.0.0.0:8000"]