from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import PlayerProfile


@receiver(post_save, sender=User)
def create_player_profile(sender, instance, created, **kwargs):
    """Автоматически создаём профиль игрока при создании пользователя"""
    if created:
        PlayerProfile.objects.create(user=instance)


def create_groups():
    """Создать группы Студент и Учитель"""
    student_group, _ = Group.objects.get_or_create(name='Студент')
    teacher_group, _ = Group.objects.get_or_create(name='Учитель')