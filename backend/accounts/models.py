from django.db import models
from django.contrib.auth.models import User


class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player_profile')
    current_order = models.IntegerField(default=1)
    completed_orders = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)  # Прогресс в процентах
    total_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Заказ {self.current_order}"


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    score = models.IntegerField()
    total_questions = models.IntegerField()
    passed = models.BooleanField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Тест: {self.score}/{self.total_questions}"


class GameAction(models.Model):
    """История действий в игре для защиты от накрутки"""
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='actions')
    action_type = models.CharField(max_length=50)  # install_cpu, install_ram, etc.
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.user.username} - {self.action_type}"


class Question(models.Model):
    """Вопросы теста по комплектующим ПК"""
    COMPONENT_CHOICES = [
        ('cpu', 'Процессор'),
        ('motherboard', 'Материнская плата'),
        ('gpu', 'Видеокарта'),
        ('ram', 'ОЗУ'),
        ('storage', 'SSD/HDD'),
        ('psu', 'Блок питания'),
        ('cooling', 'Система охлаждения'),
        ('case', 'Корпус'),
    ]

    text = models.TextField(verbose_name='Текст вопроса')
    component = models.CharField(max_length=20, choices=COMPONENT_CHOICES, verbose_name='Компонент')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.get_component_display()}: {self.text[:50]}"


class Answer(models.Model):
    """Варианты ответов для вопросов"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255, verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения')

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.text} ({'✓' if self.is_correct else '✗'})"