from rest_framework import generics
from .models import Recommendation
from .serializers import RecommendationSerializer, RecommendationCreateSerializer


class RecommendationListCreateView(generics.ListCreateAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecommendationCreateSerializer
        return RecommendationSerializer


class RecommendationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RecommendationCreateSerializer
        return RecommendationSerializer
