"""
Admin configuration for organizations app.
"""
from django.contrib import admin
from .models import Organization, Team


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin configuration for Organization model."""
    list_display = ['name', 'email', 'city', 'country', 'size', 'owner', 'is_active', 'created_at']
    list_filter = ['size', 'industry', 'is_active', 'country', 'created_at']
    search_fields = ['name', 'email', 'city', 'country', 'industry']
    ordering = ['-created_at']
    filter_horizontal = ['administrators']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description', 'email', 'phone', 'website', 'logo')
        }),
        ('Ubicación', {
            'fields': ('address', 'city', 'country')
        }),
        ('Información Empresarial', {
            'fields': ('industry', 'size')
        }),
        ('Relaciones', {
            'fields': ('owner', 'administrators')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin configuration for Team model."""
    list_display = ['name', 'organization', 'team_lead', 'department', 'member_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'department', 'created_at', 'organization']
    search_fields = ['name', 'description', 'department', 'project', 'organization__name']
    ordering = ['-created_at']
    filter_horizontal = ['members']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description', 'organization')
        }),
        ('Información del Equipo', {
            'fields': ('department', 'project', 'team_lead')
        }),
        ('Miembros', {
            'fields': ('members',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
    )
    
    def member_count(self, obj):
        """Display member count in list."""
        return obj.members.count()
    member_count.short_description = 'Miembros'