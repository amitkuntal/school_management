from .views import LoginView, RegisterView, register1
from django.urls import path, include


urlpatterns = [
    path('login/',LoginView.as_view()),
    path('register/1/', register1),
    path('register/',RegisterView.as_view())
]
