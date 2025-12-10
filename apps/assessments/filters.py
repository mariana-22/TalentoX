from django_filters import rest_framework as filters
from .models import Assessment, Question

class AssessmentFilter(filters.FilterSet):
    """Filtros para evaluaciones"""
    title = filters.CharFilter(lookup_expr='icontains', help_text="Buscar por título (parcial)")
    difficulty = filters.NumberFilter(help_text="Filtrar por dificultad exacta (1-5)")
    difficulty_min = filters.NumberFilter(field_name='difficulty', lookup_expr='gte', help_text="Dificultad mínima")
    difficulty_max = filters.NumberFilter(field_name='difficulty', lookup_expr='lte', help_text="Dificultad máxima")
    
    time_limit_min = filters.NumberFilter(field_name='time_limit', lookup_expr='gte', help_text="Tiempo límite mínimo (segundos)")
    time_limit_max = filters.NumberFilter(field_name='time_limit', lookup_expr='lte', help_text="Tiempo límite máximo (segundos)")
    
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte', help_text="Creadas después de esta fecha")
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte', help_text="Creadas antes de esta fecha")
    
    updated_after = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte', help_text="Actualizadas después de esta fecha")
    updated_before = filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte', help_text="Actualizadas antes de esta fecha")
    
    class Meta:
        model = Assessment
        fields = ['title', 'difficulty']


class QuestionFilter(filters.FilterSet):
    """Filtros para preguntas"""
    text = filters.CharFilter(lookup_expr='icontains', help_text="Buscar por texto de pregunta (parcial)")
    order = filters.NumberFilter(help_text="Filtrar por orden específico")
    order_min = filters.NumberFilter(field_name='order', lookup_expr='gte', help_text="Orden mínimo")
    order_max = filters.NumberFilter(field_name='order', lookup_expr='lte', help_text="Orden máximo")
    
    class Meta:
        model = Question
        fields = ['text', 'order']
