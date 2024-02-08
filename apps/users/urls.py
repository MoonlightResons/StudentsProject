from django.urls import path
from .views import StudentRegisterView, TeacherRegisterView, StudentProfileView, TeacherProfileView

urlpatterns = [
    path('registration/', StudentRegisterView.as_view(), name='student-register'),
    path('teacher/registration/', TeacherRegisterView.as_view(), name='teacher-register'),
    path('student/profile/<int:id>/', StudentProfileView.as_view(), name='student-profile'),
    path('teacher/profile/<int:id>/', TeacherProfileView.as_view(), name='teacher-profile'),
]