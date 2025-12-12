from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Category, Skill, SkillLevel
from .serializers import CategorySerializer, SkillSerializer, SkillLevelSerializer
from django.contrib.auth import get_user_model
from apps.users.permissions import IsAdminOrReadOnly, IsAdminOrEmpresaOrReadOnly

User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Categories - Admin can CRUD, others can only read.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ["name"]
    ordering_fields = ["name"]

class SkillViewSet(viewsets.ModelViewSet):
    """
    Skills - Admin can CRUD, others can only read.
    """
    queryset = Skill.objects.select_related("category").all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = {
        "category__id": ["exact"],
        "created_at": ["gte","lte"],
        "name": ["icontains"],
    }
    search_fields = ["name","description"]
    ordering_fields = ["created_at","name"]

    @action(detail=True, methods=["get"], url_path="top-users")
    def top_users(self, request, pk=None):
        skill = self.get_object()
        limit = int(request.query_params.get("limit", 5))
        qs = skill.skill_levels.select_related("user").order_by("-level")[:limit]
        data = [
            {"user_id": sl.user.id, "username": getattr(sl.user, "username", None), "level": sl.level}
            for sl in qs
        ]
        return Response(data)

    @action(detail=True, methods=["get"], url_path="levels")
    def levels(self, request, pk=None):
        skill = self.get_object()
        qs = skill.skill_levels.select_related("user").all()
        serializer = SkillLevelSerializer(qs, many=True)
        return Response(serializer.data)

class SkillLevelViewSet(viewsets.ModelViewSet):
    """
    Skill Levels - Admin and Empresa can CRUD, Aprendiz can only read.
    """
    queryset = SkillLevel.objects.select_related("user","skill").all()
    serializer_class = SkillLevelSerializer
    permission_classes = [IsAdminOrEmpresaOrReadOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {"user__id":["exact"], "skill__id":["exact"], "level":["gte","lte"]}