from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.http import HttpResponseForbidden
from .models import PlayerProfile, TestResult, GameAction


class TeacherAdminSite(admin.AdminSite):
    """Админ-панель только для учителей"""
    
    def has_permission(self, request):
        if not request.user.is_active:
            return False
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Учитель').exists()
    
    def admin_view(self, request, **kwargs):
        if not self.has_permission(request):
            return HttpResponseForbidden("Доступ только для учителей")
        return super().admin_view(request, **kwargs)


teacher_admin_site = TeacherAdminSite(name='teacher_admin')


@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_order', 'completed_orders', 'total_score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'score', 'total_questions', 'passed', 'completed_at']
    list_filter = ['passed', 'completed_at']
    search_fields = ['user__username']


@admin.register(GameAction)
class GameActionAdmin(admin.ModelAdmin):
    list_display = ['player', 'action_type', 'created_at']
    list_filter = ['action_type', 'created_at']
    search_fields = ['player__user__username']