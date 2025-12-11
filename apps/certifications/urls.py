from django.urls import path
from .views import (
    CertificationListCreateView,
    CertificationDetailView,
    GenerateCertificationView,
    CertificationHistoryView,
    CertificationVerifyView,
    UserCertificationStatsView
)

urlpatterns = [
    # CRUD de Certifications
    path('', CertificationListCreateView.as_view(), name='certification-list-create'),
    path('<int:pk>/', CertificationDetailView.as_view(), name='certification-detail'),
    
    # Endpoints especiales por usuario (según README)
    path('<int:user_id>/generate/', GenerateCertificationView.as_view(), name='certification-generate'),
    path('<int:user_id>/history/', CertificationHistoryView.as_view(), name='certification-history'),
    
    # Endpoints adicionales
    path('verify/<uuid:certificate_id>/', CertificationVerifyView.as_view(), name='certification-verify'),
    path('<int:user_id>/stats/', UserCertificationStatsView.as_view(), name='certification-stats'),
]
