from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import Student, Teacher
from .permissions import AnnonPermission
from .serializer import StudentSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class StudentRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password', 'name', 'second_name',],
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
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = Student.objects.create(
                email=request.data['email'],
                is_Student=True,
                name=request.data['name'],
                second_name=request.data['second_name'],
            )
            student.set_password(request.data['password'])
            student.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
