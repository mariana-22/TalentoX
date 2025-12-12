"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connection
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


def health_check(request):
    """Health check endpoint"""
    try:
        connection.ensure_connection()
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return JsonResponse({
        "status": "ok",
        "database": db_status,
        "version": "1.0.0"
    })


urlpatterns = [
    # Health Check
    path('health/', health_check, name='health-check'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Authentication (public endpoints)
    path('auth/', include('apps.users.auth_urls')),
    
    # App endpoints (require authentication)
    path('assessments/', include('apps.assessments.urls')),
    path('certifications/', include('apps.certifications.urls')),
    path('evidence/', include('apps.evidence.urls')),
    path('organizations/', include('apps.organizations.urls')),
    path('results/', include('apps.results.urls')),
    path('skills/', include('apps.skills.urls')),
    path('users/', include('apps.users.urls')),

]

