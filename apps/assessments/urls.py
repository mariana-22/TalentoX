from django.urls import path
from .views import (
    AssessmentListCreateView,
    AssessmentDetailView,
    StartAssessmentView, 
    SubmitAssessmentView, 
    QuestionCreateView,
    QuestionListView,
    QuestionDetailView
)

urlpatterns = [
    # CRUD de Assessments
    path('', AssessmentListCreateView.as_view(), name='assessment-list-create'),
    path('<int:pk>/', AssessmentDetailView.as_view(), name='assessment-detail'),
    
    # Endpoints especiales de Assessments
    path('<int:pk>/start/', StartAssessmentView.as_view(), name='assessment-start'),
    path('<int:pk>/submit/', SubmitAssessmentView.as_view(), name='assessment-submit'),
    
    # CRUD de Questions
    path('<int:pk>/questions/', QuestionListView.as_view(), name='question-list'),
    path('<int:pk>/questions/create/', QuestionCreateView.as_view(), name='question-create'),
    path('<int:pk>/questions/<int:question_id>/', QuestionDetailView.as_view(), name='question-detail'),
]
