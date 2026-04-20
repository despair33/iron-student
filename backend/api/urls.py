from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from accounts.models import PlayerProfile, TestResult
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from rest_framework import status


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
            'total_score': profile.total_score
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


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='api-login'),
    path('auth/logout/', LogoutView.as_view(), name='api-logout'),
    path('can-play/', CanPlayView.as_view(), name='can-play'),
    path('save-test/', SaveTestResultView.as_view(), name='save-test'),
    path('progress/', PlayerProgressView.as_view(), name='player-progress'),
    path('game/state/', GameStateView.as_view(), name='game-state'),
    path('game/progress/', GameProgressView.as_view(), name='game-progress'),
    path('game/order/', GameOrderView.as_view(), name='game-order'),
]