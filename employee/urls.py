from .views import *
from django.urls import path, include


urlpatterns = [
    path('student',RegisterStudentView.as_view()),
    path('subject',SubjectView.as_view()),
    path('homework',HomeWorkView.as_view())
    ]
