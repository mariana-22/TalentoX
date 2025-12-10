from django_filters import rest_framework as filters
from .models import Result, UserScore

class ResultFilter(filters.FilterSet):
    """Filtros para resultados"""
    user = filters.NumberFilter(help_text="Filtrar por ID de usuario")
    assessment = filters.NumberFilter(help_text="Filtrar por ID de evaluación")
    
    score_min = filters.NumberFilter(field_name='score', lookup_expr='gte', help_text="Puntaje mínimo")
    score_max = filters.NumberFilter(field_name='score', lookup_expr='lte', help_text="Puntaje máximo")
    
    correct_min = filters.NumberFilter(field_name='correct_answers', lookup_expr='gte', help_text="Respuestas correctas mínimas")
    correct_max = filters.NumberFilter(field_name='correct_answers', lookup_expr='lte', help_text="Respuestas correctas máximas")
    
    time_min = filters.NumberFilter(field_name='time_taken', lookup_expr='gte', help_text="Tiempo mínimo en segundos")
    time_max = filters.NumberFilter(field_name='time_taken', lookup_expr='lte', help_text="Tiempo máximo en segundos")
    
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte', help_text="Creados después de esta fecha")
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte', help_text="Creados antes de esta fecha")
    
    class Meta:
        model = Result
        fields = ['user', 'assessment']
