from django.urls import path
from .views import (
    ResultListCreateView,
    ResultDetailView,
    UserResultHistoryView, 
    UserImprovementsView,
    UserStatsView
)

urlpatterns = [
    # CRUD de Results
    path('', ResultListCreateView.as_view(), name='result-list-create'),
    path('<int:pk>/', ResultDetailView.as_view(), name='result-detail'),
    
    # Endpoints por usuario
    path('user/<int:id>/history/', UserResultHistoryView.as_view(), name='user-history'),
    path('user/<int:id>/improvements/', UserImprovementsView.as_view(), name='user-improvements'),
    path('user/<int:id>/stats/', UserStatsView.as_view(), name='user-stats'),
]
