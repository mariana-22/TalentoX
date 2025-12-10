from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Avg, Max, Min, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Result, UserScore
from .serializers import (
    ResultSerializer, 
    ResultCreateSerializer,
    UserScoreSerializer,
    UserStatsSerializer
)
from .filters import ResultFilter

# ==================== CRUD DE RESULTS ====================

class ResultListCreateView(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ResultFilter
    search_fields = ['user__username', 'assessment__title']
    ordering_fields = ['id', 'score', 'correct_answers', 'time_taken', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ResultCreateSerializer
        return ResultSerializer
    
    @swagger_auto_schema(
        operation_description="""Listar todos los resultados con filtros opcionales:
        
        **Filtros disponibles:**
        - user: ID del usuario
        - assessment: ID de la evaluación
        - score_min: Puntaje mínimo (0-100)
        - score_max: Puntaje máximo (0-100)
        - correct_min: Respuestas correctas mínimas
        - correct_max: Respuestas correctas máximas
        - time_min: Tiempo mínimo en segundos
        - time_max: Tiempo máximo en segundos
        - created_after: Fecha desde (YYYY-MM-DD)
        - created_before: Fecha hasta (YYYY-MM-DD)
        
        **Búsqueda:**
        - search: Buscar en nombre de usuario y título de evaluación
        
        **Ordenamiento:**
        - ordering: id, score, correct_answers, time_taken, created_at
          (usar - para descendente, ej: -score)
        """,
        responses={200: ResultSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crear un nuevo resultado de evaluación",
        request_body=ResultCreateSerializer,
        responses={
            201: ResultSerializer,
            400: openapi.Response(description="Error en validación")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    lookup_field = 'pk'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ResultCreateSerializer
        return ResultSerializer
    
    @swagger_auto_schema(
        operation_description="Obtener detalles de un resultado específico",
        responses={200: ResultSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar completamente un resultado",
        request_body=ResultCreateSerializer,
        responses={
            200: ResultSerializer,
            400: openapi.Response(description="Error en validación"),
            404: openapi.Response(description="Resultado no encontrado")
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente un resultado",
        request_body=ResultCreateSerializer,
        responses={
            200: ResultSerializer,
            400: openapi.Response(description="Error en validación"),
            404: openapi.Response(description="Resultado no encontrado")
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Eliminar un resultado",
        responses={
            204: openapi.Response(description="Resultado eliminado correctamente"),
            404: openapi.Response(description="Resultado no encontrado")
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ==================== HISTORIAL Y ESTADÍSTICAS POR USUARIO ====================

class UserResultHistoryView(generics.ListAPIView):
    serializer_class = ResultSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['id']
        return Result.objects.filter(user_id=user_id).order_by('-created_at')
    
    @swagger_auto_schema(
        operation_description="Obtener historial de resultados de un usuario",
        responses={200: ResultSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserImprovementsView(APIView):
    @swagger_auto_schema(
        operation_description="Obtener análisis y recomendaciones de mejora para un usuario",
        responses={
            200: openapi.Response(
                description="Análisis y recomendaciones",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user_score': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'recent_results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT)
                        ),
                        'improvement_areas': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT)
                        ),
                        'recommendations': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            404: openapi.Response(description="Usuario no encontrado")
        }
    )
    def get(self, request, id):
        # Obtener o crear UserScore
        try:
            user_score = UserScore.objects.get(user_id=id)
        except UserScore.DoesNotExist:
            return Response(
                {"error": "No se encontraron datos para este usuario"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Actualizar datos
        user_score.update_global_score()
        
        # Obtener últimos 5 resultados
        recent_results = Result.objects.filter(user_id=id).order_by('-created_at')[:5]
        
        # Analizar áreas de mejora
        low_scores = Result.objects.filter(user_id=id, score__lt=60).order_by('score')[:3]
        improvement_areas = []
        
        for result in low_scores:
            improvement_areas.append({
                'assessment': result.assessment.title,
                'score': result.score,
                'difficulty': result.assessment.difficulty,
                'date': result.created_at
            })
        
        # Generar recomendaciones
        if user_score.global_score < 50:
            recommendations = "Enfócate en practicar los conceptos básicos. Dedica más tiempo a cada pregunta."
        elif user_score.global_score < 70:
            recommendations = "Buen progreso. Revisa los temas donde obtuviste menor puntaje."
        else:
            recommendations = "¡Excelente trabajo! Intenta evaluaciones de mayor dificultad para seguir mejorando."
        
        return Response({
            'user_score': UserScoreSerializer(user_score).data,
            'recent_results': ResultSerializer(recent_results, many=True).data,
            'improvement_areas': improvement_areas,
            'recommendations': recommendations
        })


class UserStatsView(APIView):
    @swagger_auto_schema(
        operation_description="Obtener estadísticas detalladas de un usuario",
        responses={200: UserStatsSerializer}
    )
    def get(self, request, id):
        results = Result.objects.filter(user_id=id)
        
        if not results.exists():
            return Response(
                {"error": "No se encontraron resultados para este usuario"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        stats = results.aggregate(
            average_score=Avg('score'),
            best_score=Max('score'),
            worst_score=Min('score'),
            total_time=Sum('time_taken'),
            average_time=Avg('time_taken')
        )
        
        user = results.first().user
        
        data = {
            'user_id': id,
            'username': user.username,
            'total_assessments': results.count(),
            'average_score': round(stats['average_score'], 2) if stats['average_score'] else 0,
            'best_score': round(stats['best_score'], 2) if stats['best_score'] else 0,
            'worst_score': round(stats['worst_score'], 2) if stats['worst_score'] else 0,
            'total_time': stats['total_time'] or 0,
            'average_time': round(stats['average_time'], 2) if stats['average_time'] else 0,
        }
        
        return Response(data)
