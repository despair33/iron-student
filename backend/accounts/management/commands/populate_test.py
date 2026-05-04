from django.core.management.base import BaseCommand
from accounts.models import Question, Answer
from django.core.files import File
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Добавить 8 вопросов теста по комплектующим ПК'

    def handle(self, *args, **options):
        # Удаляем старые вопросы
        Question.objects.all().delete()

        # Путь к изображениям компонентов
        components_dir = os.path.join(settings.BASE_DIR.parent, 'frontend', 'components')

        # 1. Процессор
        q1 = Question.objects.create(
            text='Какой компонент называют "мозгом" компьютера и он выполняет вычисления?',
            component='cpu',
            order=1
        )
        self._add_image(q1, 'cpu.jpg', components_dir)
        Answer.objects.create(question=q1, text='Процессор (CPU)', is_correct=True, order=1)
        Answer.objects.create(question=q1, text='Видеокарта (GPU)', is_correct=False, order=2)
        Answer.objects.create(question=q1, text='Оперативная память (RAM)', is_correct=False, order=3)

        # 2. Материнская плата
        q2 = Question.objects.create(
            text='Какой компонент соединяет все детали компьютера и позволяет им взаимодействовать?',
            component='motherboard',
            order=2
        )
        self._add_image(q2, 'motherboard.jpg', components_dir)
        Answer.objects.create(question=q2, text='Материнская плата', is_correct=True, order=1)
        Answer.objects.create(question=q2, text='Процессор', is_correct=False, order=2)
        Answer.objects.create(question=q2, text='Блок питания', is_correct=False, order=3)

        # 3. Видеокарта
        q3 = Question.objects.create(
            text='Какой компонент отвечает за обработку графики и вывод изображения на монитор?',
            component='gpu',
            order=3
        )
        self._add_image(q3, 'gpu.jpg', components_dir)
        Answer.objects.create(question=q3, text='Видеокарта (GPU)', is_correct=True, order=1)
        Answer.objects.create(question=q3, text='Процессор (CPU)', is_correct=False, order=2)
        Answer.objects.create(question=q3, text='Звуковая карта', is_correct=False, order=3)

        # 4. ОЗУ (RAM)
        q4 = Question.objects.create(
            text='Какой компонент отвечает за временное хранение данных, которые используются в данный момент?',
            component='ram',
            order=4
        )
        self._add_image(q4, 'ram.jpg', components_dir)
        Answer.objects.create(question=q4, text='Оперативная память (RAM)', is_correct=True, order=1)
        Answer.objects.create(question=q4, text='SSD-накопитель', is_correct=False, order=2)
        Answer.objects.create(question=q4, text='Процессор', is_correct=False, order=3)

        # 5. SSD/HDD
        q5 = Question.objects.create(
            text='Какой компонент используется для долговременного хранения файлов, программ и операционной системы?',
            component='storage',
            order=5
        )
        self._add_image(q5, 'storage.jpg', components_dir)
        Answer.objects.create(question=q5, text='Накопитель (SSD/HDD)', is_correct=True, order=1)
        Answer.objects.create(question=q5, text='Оперативная память', is_correct=False, order=2)
        Answer.objects.create(question=q5, text='Процессор', is_correct=False, order=3)

        # 6. Блок питания
        q6 = Question.objects.create(
            text='Какой компонент преобразует электричество из розетки и подает питание на все детали компьютера?',
            component='psu',
            order=6
        )
        self._add_image(q6, 'psu.jpg', components_dir)
        Answer.objects.create(question=q6, text='Блок питания', is_correct=True, order=1)
        Answer.objects.create(question=q6, text='Материнская плата', is_correct=False, order=2)
        Answer.objects.create(question=q6, text='Процессор', is_correct=False, order=3)

        # 7. Система охлаждения
        q7 = Question.objects.create(
            text='Какой компонент предназначен для отвода тепла от процессора и предотвращения перегрева?',
            component='cooling',
            order=7
        )
        self._add_image(q7, 'cooling.jpg', components_dir)
        Answer.objects.create(question=q7, text='Система охлаждения (кулер/радиатор)', is_correct=True, order=1)
        Answer.objects.create(question=q7, text='Блок питания', is_correct=False, order=2)
        Answer.objects.create(question=q7, text='Видеокарта', is_correct=False, order=3)

        # 8. Корпус
        q8 = Question.objects.create(
            text='Какой компонент служит для размещения всех деталей компьютера и защищает их от внешних воздействий?',
            component='case',
            order=8
        )
        self._add_image(q8, 'case.jpg', components_dir)
        Answer.objects.create(question=q8, text='Корпус компьютера', is_correct=True, order=1)
        Answer.objects.create(question=q8, text='Блок питания', is_correct=False, order=2)
        Answer.objects.create(question=q8, text='Материнская плата', is_correct=False, order=3)

        self.stdout.write(self.style.SUCCESS('Добавлено 8 вопросов теста с изображениями'))

    def _add_image(self, question, filename, components_dir):
        image_path = os.path.join(components_dir, filename)
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                question.image.save(filename, File(f), save=False)
                question.save()
                self.stdout.write(f'  Added image: {filename}')
