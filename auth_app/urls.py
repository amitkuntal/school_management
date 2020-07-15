from .views import LoginView, register
from django.urls import path, include

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('register/',register)
]
