from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Theuser, StudentProfile, TeacherProfile
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings


class TheuserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Theuser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = Theuser
        fields = [
            'id',
            'email',
            'name',
            'second_name',
            'password',
            'password2',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didnt match!'}
            )
        return attrs

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['quote', 'contact', 'social_network', 'work_status', 'instes_radius', 'achievement']
        # Указываем, что поля необязательны
        extra_kwargs = {
            'quote': {'required': False},
            'contact': {'required': False},
            'social_network': {'required': False},
            'work_status': {'required': False},
            'instes_radius': {'required': False},
            'achievement': {'required': False},
        }


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['quote', 'contact', 'social_network']
        # Указываем, что поля необязательны
        extra_kwargs = {
            'quote': {'required': False},
            'contact': {'required': False},
            'social_network': {'required': False},
        }



