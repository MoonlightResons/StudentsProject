from django.urls import path
from .views import (
    AdminUserRegister,
    AdminCreateStudentView,
    AdminCreateTeacherView,
    AdminTeacherProfileView,
    AdminStudentProfileView,
    AdminGroupCreateView,
    AdminGroupDetailView,
    AdminEventDetailView,
    AdminCreateEventView,
    AdminUsersList,
    AdminGroupList,
    AdminEventsList,
    AdminStudentsProfile,
    AdminTeachersProfile
)

urlpatterns = [
    path('register/', AdminUserRegister.as_view(), name='admin-register'),
    path('student/create/', AdminCreateStudentView.as_view(), name='admin-student-create'),
    path('teacher/create/', AdminCreateTeacherView.as_view(), name='admin-teacher-create'),
    path('student/profile/', AdminStudentProfileView.as_view(), name='admin-student-profile'),
    path('teacher/profile/', AdminTeacherProfileView.as_view(), name='admin-teacher-profile'),
    path('group/create/', AdminGroupCreateView.as_view(), name='admin-group-create'),
    path('group/detail/', AdminGroupDetailView.as_view(), name='admin-group-detail'),
    path('event/create/', AdminCreateEventView.as_view(), name='admin-event-create'),
    path('event/detail/', AdminEventDetailView.as_view(), name='admin-event-detail'),
    path('users/list/', AdminUsersList.as_view(), name='admin-users-list'),
    path('student/profile/list/', AdminStudentsProfile.as_view(), name='admin-student-profile-list'),
    path('teacher/profile/list/', AdminTeachersProfile.as_view(), name='admin-teacher-profile-list'),
    path('group/list/', AdminGroupList.as_view(), name='admin-group-list'),
    path('event/list/', AdminEventsList.as_view(), name='admin-event-list'),
]
