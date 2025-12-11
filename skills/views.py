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

User = get_user_model()

class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # lectura para cualquiera autenticado (o público si quieres)
        if request.method in permissions.SAFE_METHODS:
            return True
        # escritura solo para staff (ajusta si quieres que sea propietario)
        return request.user and request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ["name"]
    ordering_fields = ["name"]

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.select_related("category").all()
    serializer_class = SkillSerializer
    permission_classes = [IsStaffOrReadOnly]
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
    queryset = SkillLevel.objects.select_related("user","skill").all()
    serializer_class = SkillLevelSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {"user__id":["exact"], "skill__id":["exact"], "level":["gte","lte"]}