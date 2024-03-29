from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField('email address', unique=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_Teacher = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        user_status = ""
        if self.is_Teacher:
            user_status = "Teacher"
        elif self.is_admin or self.is_superuser:
            user_status = "Admin"
        else:
            user_status = "Student"
        return f'{self.email} - {user_status}'

class Theuser(MyUser):
    name = models.CharField(max_length=255, null=False, blank=False)
    second_name = models.CharField(max_length=255, null=False, blank=False)


class StudentProfile(models.Model):
    studentuser = models.OneToOneField(Theuser, on_delete=models.CASCADE, related_name='student_profile')
    profile_avatar = models.ImageField()
    quote = models.TextField()
    contact = models.CharField(max_length=255)
    social_network = models.URLField()
    work_status = models.CharField(max_length=255)
    instes_radius = models.TextField()
    achievement = models.TextField()

    def __str__(self):
        return f'{self.studentuser}'


class TeacherProfile(models.Model):
    teacheruser = models.OneToOneField(Theuser, on_delete=models.CASCADE, related_name='teacher_profile')
    quote = models.TextField()
    teacher_avatar = models.ImageField()
    contact = models.CharField(max_length=255)
    social_network = models.URLField()

    def __str__(self):
        return self.teacheruser



