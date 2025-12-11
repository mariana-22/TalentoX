from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Assessment, Question, Option
from .serializers import (
    AssessmentSerializer, 
    AssessmentCreateSerializer,
    SubmitAnswersSerializer,
    QuestionCreateSerializer,
    QuestionSerializer
)
from .filters import AssessmentFilter, QuestionFilter

# ==================== CRUD DE ASSESSMENTS ====================

class AssessmentListCreateView(generics.ListCreateAPIView):
    queryset = Assessment.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AssessmentFilter
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title', 'difficulty', 'time_limit', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AssessmentCreateSerializer
        return AssessmentSerializer
    
    @swagger_auto_schema(
        operation_description="""Listar todas las evaluaciones con filtros opcionales:
        
        **Filtros disponibles:**
        - title: Buscar por título (parcial)
        - difficulty: Dificultad exacta (1-5)
        - difficulty_min: Dificultad mínima
        - difficulty_max: Dificultad máxima
        - time_limit_min: Tiempo mínimo en segundos
        - time_limit_max: Tiempo máximo en segundos
        - created_after: Fecha de creación desde
        - created_before: Fecha de creación hasta
        - updated_after: Fecha de actualización desde
        - updated_before: Fecha de actualización hasta
        
        **Búsqueda:**
        - search: Buscar en título y descripción
        
        **Ordenamiento:**
        - ordering: Ordenar por id, title, difficulty, time_limit, created_at, updated_at
          (usar - para orden descendente, ej: -created_at)
        """,
        responses={200: AssessmentSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crear una nueva evaluación",
        request_body=AssessmentCreateSerializer,
        responses={
            201: AssessmentSerializer,
            400: openapi.Response(description="Error en la validación de datos")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AssessmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assessment.objects.all()
    lookup_field = 'pk'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AssessmentCreateSerializer
        return AssessmentSerializer
    
    @swagger_auto_schema(
        operation_description="Obtener una evaluación específica con todas sus preguntas y opciones",
        responses={200: AssessmentSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar una evaluación completamente",
        request_body=AssessmentCreateSerializer,
        responses={
            200: AssessmentSerializer,
            400: openapi.Response(description="Error en la validación de datos"),
            404: openapi.Response(description="Evaluación no encontrada")
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente una evaluación",
        request_body=AssessmentCreateSerializer,
        responses={
            200: AssessmentSerializer,
            400: openapi.Response(description="Error en la validación de datos"),
            404: openapi.Response(description="Evaluación no encontrada")
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Eliminar una evaluación",
        responses={
            204: openapi.Response(description="Evaluación eliminada correctamente"),
            404: openapi.Response(description="Evaluación no encontrada")
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ==================== CRUD DE QUESTIONS ====================

class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = QuestionFilter
    search_fields = ['text']
    ordering_fields = ['id', 'order', 'created_at']
    ordering = ['order']
    
    def get_queryset(self):
        assessment_id = self.kwargs.get('pk')
        return Question.objects.filter(assessment_id=assessment_id)
    
    @swagger_auto_schema(
        operation_description="""Listar todas las preguntas de una evaluación con filtros:
        
        **Filtros disponibles:**
        - text: Buscar por texto de pregunta (parcial)
        - order: Orden específico
        - order_min: Orden mínimo
        - order_max: Orden máximo
        
        **Búsqueda:**
        - search: Buscar en texto de pregunta
        
        **Ordenamiento:**
        - ordering: Ordenar por id, order, created_at
          (usar - para orden descendente, ej: -order)
        """,
        responses={
            200: QuestionSerializer(many=True),
            404: openapi.Response(description="Evaluación no encontrada")
        }
    )
    def get(self, request, *args, **kwargs):
        assessment_id = self.kwargs.get('pk')
        if not Assessment.objects.filter(pk=assessment_id).exists():
            return Response(
                {"error": f"Evaluación con id {assessment_id} no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        return super().get(request, *args, **kwargs)


class QuestionCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Agregar una pregunta con opciones a una evaluación",
        request_body=QuestionCreateSerializer,
        responses={
            201: openapi.Response(
                description="Pregunta creada correctamente",
                schema=QuestionSerializer
            ),
            400: openapi.Response(description="Error en la validación de datos"),
            404: openapi.Response(description="Evaluación no encontrada"),
        }
    )
    def post(self, request, pk):
        # Verificar que la evaluación existe
        try:
            assessment = Assessment.objects.get(pk=pk)
        except Assessment.DoesNotExist:
            return Response(
                {"error": f"Evaluación con id {pk} no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = QuestionCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            # Agregar el assessment al crear la pregunta
            question = serializer.save(assessment=assessment)
            
            # Serializar la pregunta creada para devolverla
            response_serializer = QuestionSerializer(question)
            
            return Response(
                {
                    "message": "Pregunta creada correctamente",
                    "question": response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    lookup_field = 'question_id'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return QuestionCreateSerializer
        return QuestionSerializer
    
    def get_object(self):
        assessment_id = self.kwargs.get('pk')
        question_id = self.kwargs.get('question_id')
        try:
            return Question.objects.get(id=question_id, assessment_id=assessment_id)
        except Question.DoesNotExist:
            return None
    
    @swagger_auto_schema(
        operation_description="Obtener una pregunta específica",
        responses={
            200: QuestionSerializer,
            404: openapi.Response(description="Pregunta no encontrada")
        }
    )
    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return Response(
                {"error": "Pregunta no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Actualizar completamente una pregunta",
        request_body=QuestionCreateSerializer,
        responses={
            200: QuestionSerializer,
            400: openapi.Response(description="Error en la validación de datos"),
            404: openapi.Response(description="Pregunta no encontrada")
        }
    )
    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return Response(
                {"error": "Pregunta no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = QuestionCreateSerializer(obj, data=request.data)
        if serializer.is_valid():
            # Eliminar opciones anteriores
            obj.options.all().delete()
            # Guardar nueva pregunta con opciones
            question = serializer.save()
            response_serializer = QuestionSerializer(question)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente una pregunta",
        request_body=QuestionCreateSerializer,
        responses={
            200: QuestionSerializer,
            400: openapi.Response(description="Error en la validación de datos"),
            404: openapi.Response(description="Pregunta no encontrada")
        }
    )
    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return Response(
                {"error": "Pregunta no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = QuestionCreateSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            if 'options' in request.data:
                obj.options.all().delete()
            question = serializer.save()
            response_serializer = QuestionSerializer(question)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Eliminar una pregunta",
        responses={
            204: openapi.Response(description="Pregunta eliminada correctamente"),
            404: openapi.Response(description="Pregunta no encontrada")
        }
    )
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return Response(
                {"error": "Pregunta no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== ENDPOINTS ESPECIALES ====================

class StartAssessmentView(generics.RetrieveAPIView):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    lookup_field = 'pk'
    
    @swagger_auto_schema(
        operation_description="Iniciar una evaluación - obtiene todas sus preguntas y opciones",
        responses={200: AssessmentSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubmitAssessmentView(APIView):
    @swagger_auto_schema(
        operation_description="Enviar una respuesta a una pregunta de la evaluación",
        request_body=SubmitAnswersSerializer,
        responses={
            200: openapi.Response(
                description="Respuesta procesada correctamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'assessment_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'question_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'option_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'is_correct': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    }
                )
            ),
            400: openapi.Response(description="Error en la validación de datos"),
            404: openapi.Response(description="Evaluación, pregunta u opción no encontrada"),
        }
    )
    def post(self, request, pk):
        serializer = SubmitAnswersSerializer(data=request.data)
        
        if serializer.is_valid():
            question_id = serializer.validated_data.get("question_id")
            option_id = serializer.validated_data.get("option_id")
            
            # Validar que la evaluación existe
            try:
                assessment = Assessment.objects.get(pk=pk)
            except Assessment.DoesNotExist:
                return Response(
                    {"error": f"Evaluación con id {pk} no encontrada"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Validar que la pregunta existe y pertenece a la evaluación
            try:
                question = Question.objects.get(id=question_id, assessment=assessment)
            except Question.DoesNotExist:
                return Response(
                    {"error": f"Pregunta con id {question_id} no encontrada en esta evaluación"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Validar que la opción existe y pertenece a la pregunta
            try:
                option = Option.objects.get(id=option_id, question=question)
            except Option.DoesNotExist:
                return Response(
                    {"error": f"Opción con id {option_id} no encontrada para esta pregunta"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Verificar si la respuesta es correcta
            is_correct = option.is_correct
            
            result = {
                "message": "Respuesta recibida y procesada correctamente",
                "assessment_id": pk,
                "question_id": question_id,
                "option_id": option_id,
                "is_correct": is_correct,
            }
            
            return Response(result, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

