import time
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from .models import Theuser, StudentProfile, MyUser, TeacherProfile
from .permissions import AnnonPermission, ProfileOwnerPermission
from rest_framework.permissions import IsAuthenticated
from .serializer import TheuserRegisterSerializer, StudentProfileSerializer, TeacherProfileSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from selenium import webdriver


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
        operation_description="Register a new student"
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
        student = StudentProfile.objects.get(id=id)
        serializer = StudentProfileSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

        # # try:
        # driver.get("https://www.google.com")
        # print("Page title was '{}'".format(driver.title))

        # finally:
        #     driver.quit()

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
            required=['quote', 'contact', 'social_network', 'work_status', 'achievement', 'instes_radius'],
            properties={
                'quote': openapi.Schema(type=openapi.TYPE_STRING),
                'contact': openapi.Schema(type=openapi.TYPE_STRING),
                'social_network': openapi.Schema(type=openapi.TYPE_STRING),
                'work_status': openapi.Schema(type=openapi.TYPE_STRING),
                'achievement': openapi.Schema(type=openapi.TYPE_STRING),
                'instes_radius': openapi.Schema(type=openapi.TYPE_STRING),
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
            required=['quote', 'contact', 'social_network'],
            properties={
                'quote': openapi.Schema(type=openapi.TYPE_STRING),
                'contact': openapi.Schema(type=openapi.TYPE_STRING),
                'social_network': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'OK', 400: 'Invalid Data'},
        operation_description="Update student profile"
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





