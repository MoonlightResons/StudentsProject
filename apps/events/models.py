from django.db import models
from apps.users.models import MyUser


class Event(models.Model):
    event_owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    event_description = models.TextField()
    event_date = models.DateTimeField()
    event_place = models.CharField(max_length=255)

    def __str__(self):
        return self.event_name