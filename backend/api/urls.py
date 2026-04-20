from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User, Group
from accounts.models import PlayerProfile, TestResult
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from rest_framework import status


def is_teacher(user):
    return user.is_superuser or user.groups.filter(name='Учитель').exists()


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """Логин через API (для Unity/других клиентов)"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({
                'success': True,
                'username': user.username,
                'message': 'Login successful'
            })
        
        return Response({
            'success': False,
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'success': True, 'message': 'Logged out'})


@method_decorator(csrf_exempt, name='dispatch')
class CanPlayView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        last_test = TestResult.objects.filter(user=request.user).order_by('-completed_at').first()
        
        if last_test and last_test.passed:
            return Response({
                'can_play': True,
                'test_passed': True,
                'test_score': last_test.score
            })
        
        return Response({
            'can_play': False,
            'test_passed': False,
            'message': 'Спочатку пройдіть тест'
        })


@method_decorator(csrf_exempt, name='dispatch')
class SaveTestResultView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        score = request.data.get('score')
        total = request.data.get('total')
        
        passed = (score / total) >= 0.5 if total > 0 else False
        
        test_result = TestResult.objects.create(
            user=request.user,
            score=score,
            total_questions=total,
            passed=passed
        )
        
        return Response({
            'success': True,
            'passed': passed,
            'score': score,
            'total': total
        })


@method_decorator(csrf_exempt, name='dispatch')
class PlayerProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.player_profile
        
        return Response({
            'username': request.user.username,
            'current_order': profile.current_order,
            'completed_orders': profile.completed_orders,
            'total_score': profile.total_score,
            'progress': profile.progress
        })


@method_decorator(csrf_exempt, name='dispatch')
class GameStateView(APIView):
    """Получить состояние игры"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.player_profile
        
        return Response({
            'progress': profile.progress,
            'current_order': profile.current_order,
            'completed_orders': profile.completed_orders
        })


@method_decorator(csrf_exempt, name='dispatch')
class GameProgressView(APIView):
    """Добавить прогресс ИЛИ completed orders"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = request.user.player_profile
        
        # Добавить к прогрессу (в процентах)
        add_progress = request.data.get('add_progress', 0)
        if add_progress > 0:
            profile.progress = min(100, profile.progress + int(add_progress))
            profile.save()
            return Response({
                'success': True,
                'progress': profile.progress
            })
        
        # ИЛИ добавить к выполненным заказам
        add_orders = request.data.get('add_orders', 0)
        if add_orders > 0:
            profile.completed_orders += int(add_orders)
            profile.save()
            return Response({
                'success': True,
                'completed_orders': profile.completed_orders
            })
        
        return Response({'success': False, 'error': 'No valid action'})


@method_decorator(csrf_exempt, name='dispatch')
class GameOrderView(APIView):
    """Обновить текущий заказ"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = request.data.get('order')
        
        if order:
            profile = request.user.player_profile
            profile.current_order = order
            profile.save()
        
        return Response({
            'success': True,
            'current_order': request.user.player_profile.current_order
        })


class TeacherPermission(IsAuthenticated):
    """Разрешение только для учителей"""
    
    def has_permission(self, request, view):
        return super().has_permission(request, view) and is_teacher(request.user)


@method_decorator(csrf_exempt, name='dispatch')
class StudentListView(APIView):
    """Список всех студентов (только для учителей)"""
    permission_classes = [TeacherPermission]

    def get(self, request):
        students = User.objects.filter(groups__name='Студент').distinct()
        
        data = []
        for student in students:
            profile = student.player_profile
            last_test = TestResult.objects.filter(user=student).order_by('-completed_at').first()
            
            data.append({
                'id': student.id,
                'username': student.username,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'test_score': f"{last_test.score}/{last_test.total_questions}" if last_test else None,
                'test_passed': last_test.passed if last_test else None,
                'current_order': profile.current_order,
                'completed_orders': profile.completed_orders,
                'progress': profile.progress,
            })
        
        return Response({'students': data})


@method_decorator(csrf_exempt, name='dispatch')
class CreateStudentView(APIView):
    """Создать студента (только для учителей)"""
    permission_classes = [TeacherPermission]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        
        if not username or not password:
            return Response({
                'success': False,
                'error': 'Username and password required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({
                'success': False,
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        student_group = Group.objects.get(name='Студент')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.groups.add(student_group)
        
        return Response({
            'success': True,
            'student': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserRoleView(APIView):
    """Получить роль текущего пользователя"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'is_teacher': is_teacher(request.user),
            'is_student': request.user.groups.filter(name='Студент').exists(),
            'username': request.user.username
        })


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='api-login'),
    path('auth/logout/', LogoutView.as_view(), name='api-logout'),
    path('can-play/', CanPlayView.as_view(), name='can-play'),
    path('save-test/', SaveTestResultView.as_view(), name='save-test'),
    path('progress/', PlayerProgressView.as_view(), name='player-progress'),
    path('game/state/', GameStateView.as_view(), name='game-state'),
    path('game/progress/', GameProgressView.as_view(), name='game-progress'),
    path('game/order/', GameOrderView.as_view(), name='game-order'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/create/', CreateStudentView.as_view(), name='create-student'),
    path('user/role/', UserRoleView.as_view(), name='user-role'),
]