from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Evidence
from .serializers import EvidenceSerializer

class EvidenceViewSet(viewsets.ModelViewSet):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer

    @action(detail=False, url_path=r'user/(?P<user_id>\d+)')
    def by_user(self, request, user_id=None):
        evidences = self.queryset.filter(user_id=user_id)
        serializer = self.get_serializer(evidences, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path=r'skill/(?P<skill_id>\d+)')
    def by_skill(self, request, skill_id=None):
        evidences = self.queryset.filter(skill_id=skill_id)
        serializer = self.get_serializer(evidences, many=True)
        return Response(serializer.data)
