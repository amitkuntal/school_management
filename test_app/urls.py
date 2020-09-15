from .views import *
from django.urls import path, include


urlpatterns = [
    path('tests/', Tests.as_view()),
    path('tests/update', TestUpdate.as_view()),
    path('tests/question', Questions.as_view()),
    path('tests/question/update', QuestionUpdate.as_view()),
    path('tests/get/question/count',QuestionCount.as_view())
    ]
