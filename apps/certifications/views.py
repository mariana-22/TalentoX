from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Avg, Sum, Count
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Certification
from .serializers import (
    CertificationSerializer,
    CertificationCreateSerializer,
    CertificationGenerateSerializer,
    CertificationHistorySerializer
)
from .filters import CertificationFilter
from apps.users.permissions import IsAdminOrEmpresaOrReadOnly, CanManageResults

User = get_user_model()


# ==================== CRUD DE CERTIFICATIONS ====================

class CertificationListCreateView(generics.ListCreateAPIView):
    """
    Listar y crear certificaciones.
    - Admin/Empresa: Full access to all certifications
    - Aprendiz: Can only view their own certifications
    """
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CertificationFilter
    search_fields = ['user__username', 'title', 'description']
    ordering_fields = ['id', 'level', 'total_score', 'issued_at', 'expires_at']
    ordering = ['-issued_at']
    permission_classes = [CanManageResults]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'empresa']:
            return Certification.objects.all()
        return Certification.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CertificationCreateSerializer
        return CertificationSerializer
    
    @swagger_auto_schema(
        operation_description="""Listar todas las certificaciones con filtros opcionales:
        
        **Filtros disponibles:**
        - user: ID del usuario
        - level: Nivel de certificación (0-5)
        - level_min: Nivel mínimo
        - level_max: Nivel máximo
        - score_min: Puntaje mínimo (0-100)
        - score_max: Puntaje máximo (0-100)
        - status: Estado (pending, active, expired, revoked)
        - issued_after: Fecha de emisión desde (YYYY-MM-DD)
        - issued_before: Fecha de emisión hasta (YYYY-MM-DD)
        
        **Búsqueda:**
        - search: Buscar en nombre de usuario, título y descripción
        
        **Ordenamiento:**
        - ordering: Ordenar por id, level, total_score, issued_at, expires_at
        """,
        operation_summary="Listar certificaciones"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crear una nueva certificación",
        operation_summary="Crear certificación"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CertificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar una certificación.
    - Admin/Empresa: Full access
    - Aprendiz: Read only (their own certifications)
    """
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [CanManageResults]
    
    @swagger_auto_schema(
        operation_description="Obtener detalles de una certificación específica",
        operation_summary="Detalle de certificación"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar una certificación existente",
        operation_summary="Actualizar certificación"
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente una certificación",
        operation_summary="Actualizar parcial"
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Eliminar una certificación",
        operation_summary="Eliminar certificación"
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ==================== ENDPOINTS ESPECIALES POR USUARIO ====================

class GenerateCertificationView(APIView):
    """
    Generar una certificación para un usuario basada en sus resultados.
    Endpoint: /certifications/{user_id}/generate/
    - Only Admin and Empresa can generate certifications
    """
    permission_classes = [IsAdminOrEmpresaOrReadOnly]
    
    @swagger_auto_schema(
        operation_description="""Genera una nueva certificación para el usuario basándose en:
        - Resultados de evaluaciones completadas
        - Puntaje promedio global
        - Evidencias asociadas
        
        El nivel de certificación se calcula automáticamente según el puntaje:
        - 0-19: Sin Certificar
        - 20-39: Novato
        - 40-59: Aprendiz
        - 60-74: Competente
        - 75-89: Avanzado
        - 90-100: Experto
        """,
        operation_summary="Generar certificación para usuario",
        request_body=CertificationGenerateSerializer,
        responses={
            201: openapi.Response(
                description="Certificación generada exitosamente",
                schema=CertificationSerializer
            ),
            400: "Datos inválidos o usuario sin resultados",
            404: "Usuario no encontrado"
        }
    )
    def post(self, request, user_id):
        # Verificar que el usuario existe
        user = get_object_or_404(User, pk=user_id)
        
        # Validar datos de entrada
        serializer = CertificationGenerateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener estadísticas del usuario desde results
        from apps.results.models import Result, UserScore
        
        results = Result.objects.filter(user=user)
        
        if not results.exists():
            return Response(
                {"error": "El usuario no tiene resultados de evaluaciones para generar una certificación"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calcular estadísticas
        stats = results.aggregate(
            avg_score=Avg('score'),
            total_assessments=Count('id'),
            total_correct=Sum('correct_answers'),
            total_questions=Sum('total_questions')
        )
        
        # Crear la certificación
        certification = Certification.objects.create(
            user=user,
            title=serializer.validated_data['title'],
            description=serializer.validated_data.get('description', ''),
            total_score=stats['avg_score'] or 0,
            assessments_completed=stats['total_assessments'],
            evidence_links=serializer.validated_data.get('evidence_links', ''),
            expires_at=serializer.validated_data.get('expires_at')
        )
        
        # Calcular y guardar el nivel
        certification.calculate_level()
        certification.save()
        
        # Devolver la certificación creada
        response_serializer = CertificationSerializer(certification)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CertificationHistoryView(generics.ListAPIView):
    """
    Historial de certificaciones de un usuario.
    Endpoint: /certifications/{user_id}/history/
    """
    serializer_class = CertificationHistorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CertificationFilter
    ordering_fields = ['level', 'total_score', 'issued_at']
    ordering = ['-issued_at']
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Certification.objects.filter(user_id=user_id)
    
    @swagger_auto_schema(
        operation_description="""Obtener el historial completo de certificaciones de un usuario.
        
        Incluye todas las certificaciones emitidas, incluyendo:
        - Certificaciones activas
        - Certificaciones expiradas
        - Certificaciones revocadas
        
        **Filtros disponibles:**
        - level: Filtrar por nivel específico
        - status: Filtrar por estado
        - issued_after: Certificaciones emitidas después de fecha
        - issued_before: Certificaciones emitidas antes de fecha
        """,
        operation_summary="Historial de certificaciones del usuario",
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_PATH,
                description="ID del usuario",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: CertificationHistorySerializer(many=True),
            404: "Usuario no encontrado"
        }
    )
    def get(self, request, *args, **kwargs):
        # Verificar que el usuario existe
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, pk=user_id)
        return super().get(request, *args, **kwargs)


# ==================== ENDPOINTS ADICIONALES ====================

class CertificationVerifyView(APIView):
    """Verificar validez de una certificación por su UUID"""
    
    @swagger_auto_schema(
        operation_description="Verificar si una certificación es válida por su UUID",
        operation_summary="Verificar certificación",
        responses={
            200: openapi.Response(
                description="Estado de la certificación",
                examples={
                    "application/json": {
                        "certificate_id": "uuid-string",
                        "is_valid": True,
                        "status": "active",
                        "user": "username",
                        "title": "Certificación título",
                        "level": 3,
                        "issued_at": "2024-01-01T00:00:00Z"
                    }
                }
            ),
            404: "Certificación no encontrada"
        }
    )
    def get(self, request, certificate_id):
        certification = get_object_or_404(Certification, certificate_id=certificate_id)
        
        return Response({
            "certificate_id": str(certification.certificate_id),
            "is_valid": certification.is_valid(),
            "status": certification.status,
            "status_display": certification.get_status_display(),
            "user": certification.user.username,
            "title": certification.title,
            "level": certification.level,
            "level_display": certification.get_level_display(),
            "total_score": certification.total_score,
            "issued_at": certification.issued_at,
            "expires_at": certification.expires_at
        })


class UserCertificationStatsView(APIView):
    """Estadísticas de certificaciones de un usuario"""
    
    @swagger_auto_schema(
        operation_description="Obtener estadísticas de certificaciones del usuario",
        operation_summary="Estadísticas de certificaciones",
        responses={
            200: openapi.Response(
                description="Estadísticas del usuario",
                examples={
                    "application/json": {
                        "user_id": 1,
                        "username": "usuario",
                        "total_certifications": 5,
                        "active_certifications": 4,
                        "highest_level": 4,
                        "average_score": 75.5
                    }
                }
            ),
            404: "Usuario no encontrado"
        }
    )
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        
        certifications = Certification.objects.filter(user=user)
        active_certs = certifications.filter(status='active')
        
        stats = certifications.aggregate(
            total=Count('id'),
            avg_score=Avg('total_score')
        )
        
        active_stats = active_certs.aggregate(
            active_count=Count('id'),
            highest_level=models.Max('level')
        )
        
        # Importar models para Max
        from django.db.models import Max
        highest = active_certs.aggregate(highest=Max('level'))
        
        return Response({
            "user_id": user.id,
            "username": user.username,
            "total_certifications": stats['total'] or 0,
            "active_certifications": active_stats['active_count'] or 0,
            "highest_level": highest['highest'] or 0,
            "average_score": round(stats['avg_score'] or 0, 2)
        })
