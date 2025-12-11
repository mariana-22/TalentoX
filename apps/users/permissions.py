from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsEmpresa(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "empresa"


class IsAprendiz(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "aprendiz"
