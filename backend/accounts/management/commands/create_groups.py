from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Создать группы Студент и Учитель'

    def handle(self, *args, **options):
        student_group, created = Group.objects.get_or_create(name='Студент')
        teacher_group, created = Group.objects.get_or_create(name='Учитель')
        
        if created:
            self.stdout.write(self.style.SUCCESS('Группы созданы'))
        else:
            self.stdout.write('Группы уже существуют')