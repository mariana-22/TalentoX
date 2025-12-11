from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .models import Organization, Team
from .serializers import (
    OrganizationListSerializer, OrganizationDetailSerializer,
    OrganizationCreateSerializer, OrganizationUpdateSerializer,
    TeamListSerializer, TeamCreateSerializer, TeamUpdateSerializer
)
from .filters import OrganizationFilter
from apps.users.models import User


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OrganizationFilter
    search_fields = ['name', 'description', 'city', 'country']
    ordering_fields = ['created_at', 'name', 'size']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return OrganizationListSerializer
        elif self.action == 'create':
            return OrganizationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrganizationUpdateSerializer
        return OrganizationDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Organization.objects.all()
        elif user.role == 'empresa':
            return Organization.objects.filter(owner=user) | Organization.objects.filter(administrators=user)
        return Organization.objects.filter(teams__members=user).distinct()

    @extend_schema(
        operation_id='organizations_list',
        summary='Listar organizaciones',
        description='Obtiene la lista de organizaciones con opciones de filtrado y búsqueda'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id='organizations_create',
        summary='Crear organización',
        description='Crea una nueva organización en el sistema'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        operation_id='organizations_read',
        summary='Obtener organización',
        description='Obtiene los detalles de una organización específica'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id='organizations_update',
        summary='Actualizar organización',
        description='Actualiza todos los datos de una organización'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        operation_id='organizations_partial_update',
        summary='Actualizar parcialmente',
        description='Actualiza algunos datos de una organización'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id='organizations_delete',
        summary='Eliminar organización',
        description='Elimina una organización del sistema'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        operation_id='organizations_members_list',
        summary='Listar miembros',
        description='Obtiene todos los miembros de la organización'
    )
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Obtener todos los miembros de una organización"""
        organization = self.get_object()
        teams = organization.teams.all()
        members_data = []
        
        for team in teams:
            for member in team.members.all():
                members_data.append({
                    "id": member.id,
                    "username": member.username,
                    "email": member.email,
                    "full_name": member.full_name,
                    "team": team.name,
                    "team_id": team.id
                })
        
        return Response({
            "organization": organization.name,
            "total_members": len(set([m['id'] for m in members_data])),
            "members": members_data
        })

    @extend_schema(
        operation_id='organizations_teams_list',
        summary='Listar equipos',
        description='Obtiene todos los equipos de la organización'
    )
    @action(detail=True, methods=['get'])
    def teams(self, request, pk=None):
        """Obtener todos los equipos de una organización"""
        organization = self.get_object()
        teams = organization.teams.all()
        serializer = TeamListSerializer(teams, many=True)
        return Response(serializer.data)

    @extend_schema(
        operation_id='organizations_teams_create',
        summary='Crear equipo',
        description='Crea un nuevo equipo en la organización'
    )
    @action(detail=True, methods=['post'])
    def create_team(self, request, pk=None):
        """Crear un nuevo equipo para esta organización"""
        organization = self.get_object()
        serializer = TeamCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(organization=organization)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'], url_path='teams/(?P<team_id>[^/.]+)')
    def update_team(self, request, pk=None, team_id=None):
        """Actualizar un equipo"""
        organization = self.get_object()
        try:
            team = organization.teams.get(id=team_id)
        except Team.DoesNotExist:
            return Response({'error': 'Equipo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TeamUpdateSerializer(team, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='teams/(?P<team_id>[^/.]+)')
    def delete_team(self, request, pk=None, team_id=None):
        """Eliminar un equipo"""
        organization = self.get_object()
        try:
            team = organization.teams.get(id=team_id)
            team.delete()
            return Response({'message': 'Equipo eliminado'}, status=status.HTTP_204_NO_CONTENT)
        except Team.DoesNotExist:
            return Response({'error': 'Equipo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='teams/(?P<team_id>[^/.]+)/add_member')
    def add_team_member(self, request, pk=None, team_id=None):
        """Agregar miembro a un equipo"""
        organization = self.get_object()
        try:
            team = organization.teams.get(id=team_id)
            user_id = request.data.get('user_id')
            
            if not user_id:
                return Response({'error': 'user_id requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = get_object_or_404(User, id=user_id)
            team.members.add(user)
            return Response({'message': f'{user.username} agregado al equipo'})
        except Team.DoesNotExist:
            return Response({'error': 'Equipo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='teams/(?P<team_id>[^/.]+)/remove_member')
    def remove_team_member(self, request, pk=None, team_id=None):
        """Remover miembro de un equipo"""
        organization = self.get_object()
        try:
            team = organization.teams.get(id=team_id)
            user_id = request.data.get('user_id')
            
            if not user_id:
                return Response({'error': 'user_id requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = get_object_or_404(User, id=user_id)
            team.members.remove(user)
            return Response({'message': f'{user.username} removido del equipo'})
        except Team.DoesNotExist:
            return Response({'error': 'Equipo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        operation_id='organizations_add_admin_create',
        summary='Agregar administrador',
        description='Agrega un usuario como administrador de la organización'
    )
    @action(detail=True, methods=['post'])
    def add_admin(self, request, pk=None):
        """Agregar administrador a la organización"""
        organization = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=user_id)
        organization.administrators.add(user)
        
        return Response({'message': f'{user.username} agregado como administrador'})

    @extend_schema(
        operation_id='organizations_remove_admin_create',
        summary='Remover administrador',
        description='Remueve un usuario de los administradores de la organización'
    )
    @action(detail=True, methods=['post'])
    def remove_admin(self, request, pk=None):
        """Remover administrador de la organización"""
        organization = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=user_id)
        organization.administrators.remove(user)
        
        return Response({'message': f'{user.username} removido como administrador'})
