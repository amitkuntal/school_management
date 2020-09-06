from .views import *
from django.urls import path, include


urlpatterns = [
    path('register/student', RegisterStudentView.as_view()),
    path('class', RegisterClassView.as_view()),
    path('class/students', GetAllStudentFromClass.as_view()),
    path('employee', RegisterEmployeeView.as_view()),
    path('subject', SubjectView.as_view()),
    path('class/subject',ClassSubjectView.as_view()),
    path('school/education',AddSchoolEducationView.as_view()),
    path('get/subject/video',GetSchoolEducationView.as_view()),
    path('timetable',TimeTableView.as_view()),
    path('get/student/profile', GetStudentProfile.as_view()),
    path('get/employee/profile', GetEmployeeProfile.as_view()),
    path('profile', SchoolProfile.as_view())
    ]
