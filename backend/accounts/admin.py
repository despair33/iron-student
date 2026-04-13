from django.contrib import admin
from .models import PlayerProfile, TestResult, GameAction


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