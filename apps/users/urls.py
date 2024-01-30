from django.urls import path
from .views import StudentRegisterView

urlpatterns = [
    path('student/registration/', StudentRegisterView.as_view(), name='student-register')
]