from django.db import models
from apps.users.models import MyUser


class Group(models.Model):
    group_owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='group_owner', blank=True)
    group_name = models.CharField(max_length=55)
    group_type = models.CharField(max_length=55)
    group_url = models.URLField()
    group_description = models.TextField()
    group_year = models.CharField(max_length=20)
    group_member = models.ManyToManyField(MyUser, blank=True, related_name='group_member')

    def __str__(self):
        return self.group_name
