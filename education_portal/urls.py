from .views import *
from django.urls import path, include


urlpatterns = [
    path('test/',TestView.as_view())
    ]
