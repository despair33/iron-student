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