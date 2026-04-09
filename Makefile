run:
	cd backend && source venv/bin/activate && python manage.py runserver 0.0.0.0:8000

migrate:
	cd backend && source venv/bin/activate && python manage.py makemigrations && python manage.py migrate

install:
	cd backend && source venv/bin/activate && pip install -r requirements.txt
