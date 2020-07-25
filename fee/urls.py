from .views import *
from django.urls import path, include


urlpatterns = [
    path('fee/structure',RegisterFeeView.as_view()),
    path('class/fee/structure/<str:classid>',GetFeeStructureByClassid.as_view())
    ]
