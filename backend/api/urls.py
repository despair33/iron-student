from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from accounts.models import PlayerProfile, TestResult
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


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


urlpatterns = [
    path('can-play/', CanPlayView.as_view(), name='can-play'),
    path('save-test/', SaveTestResultView.as_view(), name='save-test'),
    path('progress/', PlayerProgressView.as_view(), name='player-progress'),
]