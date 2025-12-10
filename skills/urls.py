from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, SkillViewSet, SkillLevelViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("skills", SkillViewSet, basename="skill")
router.register("skill-levels", SkillLevelViewSet, basename="skilllevel")

urlpatterns = router.urls