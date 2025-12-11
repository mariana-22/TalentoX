from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiExample

from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    UserCreateSerializer, UserUpdateSerializer, ProfileUpdateSerializer
)
from .models import User, Profile
from .filters import UserFilter
from .permissions import IsAdmin


@extend_schema(
    operation_id='users_register',
    summary="Registrar usuario",
    description="Crea una nueva cuenta de usuario en el sistema",
    request=RegisterSerializer,
    examples=[
        OpenApiExample(
            'Registrar usuario',
            value={
                'username': 'maria_garcia',
                'email': 'maria@example.com',
                'password': 'MiPassword123!',
                'role': 'talento'
            },
            request_only=True
        ),
    ]
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Usuario creado exitosamente"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    operation_id='users_login',
    summary="Iniciar sesión",
    description="Autentica un usuario y devuelve tokens JWT",
    request=LoginSerializer,
    examples=[
        OpenApiExample(
            'Ejemplo con username',
            value={
                'username': 'maria_garcia',
                'password': 'MiPassword123!'
            },
            request_only=True
        ),
        OpenApiExample(
            'Ejemplo con email',
            value={
                'email': 'maria@example.com',
                'password': 'MiPassword123!'
            },
            request_only=True
        ),
    ]
)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    operation_id='users_me',
    summary="Perfil actual",
    description="Obtiene, actualiza o desactiva el perfil del usuario autenticado"
)
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.is_active = False
        request.user.save()
        return Response(
            {"message": "Cuenta desactivada"}, 
            status=status.HTTP_200_OK
        )


@extend_schema(
    operation_id='users_profile_update',
    summary="Actualizar perfil",
    description="Actualiza la información del perfil del usuario autenticado"
)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = UserFilter
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'username', 'email']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdmin()]

    @extend_schema(
        operation_id='users_list',
        summary='Listar usuarios',
        description='Obtiene la lista de todos los usuarios con opciones de filtrado y búsqueda'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id='users_create',
        summary='Crear usuario',
        description='Crea un nuevo usuario en el sistema'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        operation_id='users_read',
        summary='Obtener usuario',
        description='Obtiene los detalles de un usuario específico'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id='users_update',
        summary='Actualizar usuario',
        description='Actualiza todos los datos de un usuario'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        operation_id='users_partial_update',
        summary='Actualizar parcialmente',
        description='Actualiza algunos datos de un usuario'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id='users_delete',
        summary='Eliminar usuario',
        description='Elimina un usuario del sistema'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        operation_id='users_skills_read',
        summary='Obtener habilidades',
        description='Retorna las habilidades y niveles de competencia del usuario'
    )
    @action(detail=True, methods=['get'])
    def skills(self, request, pk=None):
        """Obtener habilidades de un usuario"""
        user = self.get_object()
        # TODO: Implementar modelo de Skills
        return Response({
            "user_id": user.id,
            "username": user.username,
            "skills": [
                {"skill": "Python", "level": "Avanzado"},
                {"skill": "Django", "level": "Intermedio"},
            ]
        })
