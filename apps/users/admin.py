from django.contrib import admin
from .models import Theuser, MyUser, StudentProfile, TeacherProfile

admin.site.register(Theuser)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(MyUser)
