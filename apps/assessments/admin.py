from django.contrib import admin
from .models import Assessment, Question, Option

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'time_limit', 'created_at')
    list_filter = ('difficulty', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información General', {
            'fields': ('title', 'description')
        }),
        ('Configuración', {
            'fields': ('difficulty', 'time_limit')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'assessment', 'order')
    list_filter = ('assessment', 'created_at')
    search_fields = ('text',)
    ordering = ('assessment', 'order')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__assessment')
    search_fields = ('text', 'question__text')
