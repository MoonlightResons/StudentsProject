from django.urls import path
from .views import StudentRegisterView, TeacherRegisterView, StudentProfileView, TeacherProfileView, LoginView, RefreshTokenView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', StudentRegisterView.as_view(), name='student-register'),
    path('teacher/registration/', TeacherRegisterView.as_view(), name='teacher-register'),
    path('student/profile/<int:id>/', StudentProfileView.as_view(), name='student-profile'),
    path('teacher/profile/<int:id>/', TeacherProfileView.as_view(), name='teacher-profile'),
    path('refresh/token/', RefreshTokenView.as_view(), name='refresh-token'),
]