from django.contrib import admin
from .models import Result, UserScore

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'assessment', 'score', 'correct_answers', 'total_questions', 'time_taken', 'created_at')
    list_filter = ('created_at', 'assessment')
    search_fields = ('user__username', 'assessment__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(UserScore)
class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'global_score', 'total_assessments', 'total_correct', 'total_questions', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('updated_at',)
    ordering = ('-global_score',)
