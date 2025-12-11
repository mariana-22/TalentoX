from django.urls import path
from .views import RecommendationListCreateView, RecommendationDetailView

urlpatterns = [
    path('', RecommendationListCreateView.as_view(), name='recommendation-list-create'),
    path('<int:pk>/', RecommendationDetailView.as_view(), name='recommendation-detail'),
]
