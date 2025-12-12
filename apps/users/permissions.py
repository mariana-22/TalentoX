from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Permission for admin users - full access to everything.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsEmpresa(BasePermission):
    """
    Permission for empresa users - can evaluate and manage assessments.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "empresa"


class IsAprendiz(BasePermission):
    """
    Permission for aprendiz users - read-only access to most resources.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "aprendiz"


class IsAdminOrEmpresa(BasePermission):
    """
    Permission for admin or empresa users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "empresa"]


class IsAdminOrReadOnly(BasePermission):
    """
    Admin can do everything, others can only read.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == "admin":
            return True
        return request.method in SAFE_METHODS


class IsAdminOrEmpresaOrReadOnly(BasePermission):
    """
    Admin and empresa can do everything, aprendiz can only read.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ["admin", "empresa"]:
            return True
        return request.method in SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission: owner or admin can access.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        # Check if the object has a user field
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # Check if the object IS a user
        return obj == request.user


class IsOwnerOrAdminOrEmpresa(BasePermission):
    """
    Object-level permission: owner, admin, or empresa can access.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role in ["admin", "empresa"]:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user


class CanManageAssessments(BasePermission):
    """
    Admin and empresa can create/edit/delete assessments.
    Aprendiz can only view and take assessments.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ["admin", "empresa"]:
            return True
        # Aprendiz can only read, start, and submit
        if request.user.role == "aprendiz":
            if request.method in SAFE_METHODS:
                return True
            # Allow specific actions for aprendiz
            if hasattr(view, 'action') and view.action in ['start', 'submit']:
                return True
        return False


class CanManageResults(BasePermission):
    """
    Admin and empresa can view all results.
    Aprendiz can only view their own results.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ["admin", "empresa"]:
            return True
        # Aprendiz can only read
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.role in ["admin", "empresa"]:
            return True
        # Aprendiz can only see their own results
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False
