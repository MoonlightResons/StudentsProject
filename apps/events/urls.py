from django.urls import path
from .views import CreateEventView, EventDetailView


urlpatterns = [
    path('create/', CreateEventView.as_view(), name='create-event'),
    path('detail/<int:id>/', EventDetailView.as_view(), name='event-detail'),
]