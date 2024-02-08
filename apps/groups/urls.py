from django.urls import path
from .views import GroupCreateView, GroupDetailView, GroupMemberRequestVIew


urlpatterns = [
    path('create/', GroupCreateView.as_view(), name='create-group'),
    path('detail/<int:id>/', GroupDetailView.as_view(), name='group-detail'),
    path('request/<int:id>/', GroupMemberRequestVIew.as_view(), name="member-group-request")
]