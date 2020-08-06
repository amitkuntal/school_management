from .views import *
from django.urls import path, include


urlpatterns = [
    path('test/',TestView.as_view()),
    path('employe',EmployeeAttendanceView.as_view()),
    path('student',StudentAttendanceView.as_view()),
    path('student/self',StudentSelftAttendanceView.as_view())
    ]
