#!/bin/bash
python backend/manage.py migrate
python backend/manage.py collectstatic --noinput
python backend/manage.py create_groups
python backend/manage.py populate_test

# Создание суперпользователя, если его нет
export DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
export DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
export DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-admin}

python backend/manage.py shell -c "
from django.contrib.auth.models import User;
username = '$DJANGO_SUPERUSER_USERNAME';
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email='$DJANGO_SUPERUSER_EMAIL', password='$DJANGO_SUPERUSER_PASSWORD');
    print('Superuser created');
else:
    print('Superuser already exists');
"

python backend/manage.py runserver 0.0.0.0:8000
