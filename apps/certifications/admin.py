from django.contrib import admin
from .models import Certification


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('certificate_id', 'user', 'title', 'level', 'total_score', 'status', 'issued_at', 'expires_at')
    list_filter = ('status', 'level', 'issued_at')
    search_fields = ('user__username', 'title', 'description', 'certificate_id')
    readonly_fields = ('certificate_id', 'issued_at', 'updated_at')
    ordering = ('-issued_at',)
    
    fieldsets = (
        ('Información General', {
            'fields': ('certificate_id', 'user', 'title', 'description')
        }),
        ('Evaluación', {
            'fields': ('level', 'total_score', 'assessments_completed', 'evidence_links')
        }),
        ('Estado', {
            'fields': ('status', 'issued_at', 'expires_at', 'updated_at')
        }),
    )
