from .views import LoginView, RegisterView, register1, ProfileView,GetCountView
from django.urls import path, include


urlpatterns = [
    path('login/',LoginView.as_view()),
    path('register/',RegisterView.as_view()),
    path('profile', ProfileView.as_view()),
    path('get/count/<str:name>', GetCountView.as_view()),
    path('register/1/', register1)
]
