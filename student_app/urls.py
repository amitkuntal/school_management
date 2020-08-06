from .views import *
from django.urls import path, include


urlpatterns = [
    path('test/',TestView.as_view()),
    path('subject',SubjectView.as_view()),
    path('homework', HomeWorkView.as_view())
    ]
