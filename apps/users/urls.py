from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeView, ProfileView, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path("me/", MeView.as_view(), name='me'),
    path("me/profile/", ProfileView.as_view(), name='profile'),
    path("", include(router.urls)),
]
