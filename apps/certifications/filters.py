from django_filters import rest_framework as filters
from .models import Certification


class CertificationFilter(filters.FilterSet):
    """Filtros para certificaciones"""
    user = filters.NumberFilter(help_text="Filtrar por ID de usuario")
    level = filters.NumberFilter(help_text="Filtrar por nivel exacto (0-5)")
    
    level_min = filters.NumberFilter(field_name='level', lookup_expr='gte', help_text="Nivel mínimo")
    level_max = filters.NumberFilter(field_name='level', lookup_expr='lte', help_text="Nivel máximo")
    
    score_min = filters.NumberFilter(field_name='total_score', lookup_expr='gte', help_text="Puntaje mínimo")
    score_max = filters.NumberFilter(field_name='total_score', lookup_expr='lte', help_text="Puntaje máximo")
    
    status = filters.ChoiceFilter(choices=Certification.STATUS_CHOICES, help_text="Estado de la certificación")
    
    issued_after = filters.DateTimeFilter(field_name='issued_at', lookup_expr='gte', help_text="Emitidas después de esta fecha")
    issued_before = filters.DateTimeFilter(field_name='issued_at', lookup_expr='lte', help_text="Emitidas antes de esta fecha")
    
    expires_after = filters.DateTimeFilter(field_name='expires_at', lookup_expr='gte', help_text="Expiran después de esta fecha")
    expires_before = filters.DateTimeFilter(field_name='expires_at', lookup_expr='lte', help_text="Expiran antes de esta fecha")
    
    class Meta:
        model = Certification
        fields = ['user', 'level', 'status']
