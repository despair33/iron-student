@echo off
cd /d "%~dp0backend"
call venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
