from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Evidence
from .serializers import EvidenceSerializer
from apps.users.permissions import IsAdminOrEmpresaOrReadOnly, IsOwnerOrAdminOrEmpresa


class EvidenceViewSet(viewsets.ModelViewSet):
    """
    Evidence CRUD.
    - Admin/Empresa: Full access to all evidence
    - Aprendiz: Can create own evidence, view all, but only edit/delete own
    """
    serializer_class = EvidenceSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'empresa']:
            return Evidence.objects.all()
        # Aprendiz can see all evidence but will only be able to modify their own
        return Evidence.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'by_user', 'by_skill']:
            return [IsAuthenticated()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return [IsOwnerOrAdminOrEmpresa()]
    
    def perform_create(self, serializer):
        # Automatically assign the current user when creating evidence
        serializer.save(user=self.request.user)

    @action(detail=False, url_path=r'user/(?P<user_id>\d+)')
    def by_user(self, request, user_id=None):
        evidences = Evidence.objects.filter(user_id=user_id)
        serializer = self.get_serializer(evidences, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path=r'skill/(?P<skill_id>\d+)')
    def by_skill(self, request, skill_id=None):
        evidences = Evidence.objects.filter(skill_id=skill_id)
        serializer = self.get_serializer(evidences, many=True)
        return Response(serializer.data)
