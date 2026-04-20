import os
import django
import json
from django.test import Client
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iron-student.settings')
django.setup()

def test_game_progress():
    # 1. Создаем тестового пользователя, если его нет
    username = 'testuser'
    password = 'password123'
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password=password)
        from accounts.models import PlayerProfile
        PlayerProfile.objects.get_or_create(user=user)
    else:
        user = User.objects.get(username=username)

    client = Client()
    
    # 2. Логинимся
    client.login(username=username, password=password)
    
    # 3. Делаем POST запрос без CSRF токена
    response = client.post(
        '/api/game/progress/', 
        data=json.dumps({'add_progress': 10}),
        content_type='application/json'
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_game_progress()
