"""
Admin configuration for users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""
    list_display = ['username', 'email', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('role', 'phone')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('email', 'role', 'phone')
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profile model."""
    list_display = ['user', 'location', 'current_position', 'years_experience', 'created_at']
    list_filter = ['years_experience', 'created_at']
    search_fields = ['user__username', 'user__email', 'location', 'current_position']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Información Personal', {
            'fields': ('bio', 'avatar', 'birth_date', 'location')
        }),
        ('Información Profesional', {
            'fields': ('current_position', 'years_experience')
        }),
        ('Redes Sociales', {
            'fields': ('website', 'linkedin', 'github')
        }),
    )