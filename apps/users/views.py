import time
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from .models import Theuser, StudentProfile, MyUser, TeacherProfile
from .permissions import AnnonPermission, ProfileOwnerPermission
from rest_framework.permissions import IsAuthenticated
from .serializer import TheuserRegisterSerializer, StudentProfileSerializer, TeacherProfileSerializer, \
    MyTokenObtainPairSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from selenium import webdriver


class LoginView(TokenObtainPairView):
    permission_classes = (AnnonPermission,)
    serializer_class = MyTokenObtainPairSerializer


class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh_token'],
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'OK', 400: 'Invalid Data'},
        operation_description="Refresh token"
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)

                # Получение данных о пользователе из токена
                user_id = token.payload.get('user_id', None)
                is_admin = token.payload.get('is_staff', False)
                is_active = token.payload.get('is_active', False)
                is_Teacher = token.payload.get('is_Teacher', False)

                return Response({
                    'access_token': str(token.access_token),
                    'user_status': {
                        'user_id': user_id,
                        'is_admin': is_admin,
                        'is_active': is_active,
                        'is_Teacher': is_Teacher
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Refresh token is missing'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password', 'name', 'second_name'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'password2': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'second_name': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'OK', 400: 'Invalid Data'},
        operation_description="Register a new student"
    )

    def post(self, request):
        serializer = TheuserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            student = Theuser.objects.create(
                email=request.data['email'],
                name=request.data['name'],
                second_name=request.data['second_name'],
            )
            student.set_password(request.data['password'])
            student.save()
            StudentProfile.objects.create(studentuser=student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password', 'name', 'second_name'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'password2': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'second_name': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'OK', 400: 'Invalid Data'},
        operation_description="Register a new Teacher"
    )

    def post(self, request):
        serializer = TheuserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            teacher = Theuser.objects.create(
                email=request.data['email'],
                name=request.data['name'],
                second_name=request.data['second_name'],
                is_Teacher=True
            )
            teacher.set_password(request.data['password'])
            teacher.save()
            TeacherProfile.objects.create(teacheruser=teacher)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentProfileView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        try:
            student = StudentProfile.objects.get(id=id)
            serializer = StudentProfileSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudentProfile.DoesNotExist:
            serializer = StudentProfileSerializer(data={})
            if serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


    @classmethod
    def linkedin_login_and_work_parsing(cls, profile):
        with open("licreds.txt") as f:
            lines = f.readlines()
            LINKEDIN_LOGIN, LINKEDIN_PASSWORD = lines[0].strip(), lines[1].strip()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(options=chrome_options)


        url_login = 'https://www.linkedin.com/login/ru?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
        driver.get(url_login)
        time.sleep(2)
        login_field = driver.find_element("id", "username")
        login_field.send_keys(LINKEDIN_LOGIN)
        password_field = driver.find_element("id", "password")
        password_field.send_keys(LINKEDIN_PASSWORD)
        login_field.submit()
        time.sleep(5)

        profiles = StudentProfile.objects.all()

        for profile in profiles:
            if not profile.social_network:
                continue

            driver.get(profile.social_network)
            time.sleep(5)

            try:
                work_field = driver.find_element(By.CSS_SELECTOR, '.display-flex.align-items-center.mr1.t-bold > span')
                work_info = work_field.text.strip()
                print("Место работы для профиля {}: {}".format(profile.id, work_info))

                profile.work_status = work_info
                profile.save()
            except NoSuchElementException:
                print("Информация о месте работы не найдена на странице для профиля", profile.id)

        driver.quit()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['quote', 'contact', 'social_network', 'work_status', 'achievement', 'instes_radius', 'profile_avatar'],
            properties={
                'quote': openapi.Schema(type=openapi.TYPE_STRING),
                'contact': openapi.Schema(type=openapi.TYPE_STRING),
                'social_network': openapi.Schema(type=openapi.TYPE_STRING),
                'work_status': openapi.Schema(type=openapi.TYPE_STRING),
                'achievement': openapi.Schema(type=openapi.TYPE_STRING),
                'instes_radius': openapi.Schema(type=openapi.TYPE_STRING),
                'profile_avatar': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'OK', 400: 'Invalid Data'},
        operation_description="Update student profile"
    )

    def patch(self, request, id):
        try:
            profile = StudentProfile.objects.get(id=id)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Студент с указанным ID не найден"}, status=status.HTTP_404_NOT_FOUND)

        old_social_network = profile.social_network

        serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            new_social_network = serializer.validated_data.get('social_network', None)

            if old_social_network != new_social_network and new_social_network:
                self.__class__.linkedin_login_and_work_parsing(profile)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, id):
        student = MyUser.objects.get(id=id)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class TeacherProfileView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        student = TeacherProfile.objects.get(id=id)
        serializer = TeacherProfileSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['quote', 'contact', 'social_network', "teacher_avatar"],
            properties={
                'quote': openapi.Schema(type=openapi.TYPE_STRING),
                'contact': openapi.Schema(type=openapi.TYPE_STRING),
                'social_network': openapi.Schema(type=openapi.TYPE_STRING),
                'teacher_avatar': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'OK', 400: 'Invalid Data'},
        operation_description="Update teacher profile"
    )

    def patch(self, request, id):
        teacher = TeacherProfile.objects.get(id=id)
        serializer = TeacherProfileSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        teacher = MyUser.objects.get(id=id)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)





