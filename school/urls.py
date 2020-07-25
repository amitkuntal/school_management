from .views import *
from django.urls import path, include


urlpatterns = [
    path('register/student', RegisterStudentView.as_view()),
    path('class', RegisterClassView.as_view())
    ]
