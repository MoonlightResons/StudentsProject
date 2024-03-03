from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from apps.users.permissions import SuperUser
from apps.users.models import Theuser, StudentProfile, TeacherProfile, MyUser
from .serializer import AdminRegisterSerializer
from ..events.models import Event
from ..events.serializer import EventSerializer
from ..groups.models import Group
from ..groups.serializer import GroupSerializer, GroupDetailSerializer
from ..users.serializer import TheuserRegisterSerializer, StudentProfileSerializer, TeacherProfileSerializer, TheUserSerializer


class AdminUsersList(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = MyUser.objects.all()
    serializer_class = TheUserSerializer


class AdminStudentsProfile(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


class AdminTeachersProfile(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer


class AdminGroupList(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupDetailSerializer


class AdminEventsList(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AdminUserRegister(APIView):
    permission_classes = [SuperUser]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'name', 'password'],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "password2": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: "OK", 400: "Invalid Data"},
        operation_description="Admin User Register",
    )

    def post(self, request):
        serializer = AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            admin = Theuser.objects.create(
                email=request.data['email'],
                name=request.data['name'],
                is_staff=True
            )
            admin.set_password(request.data['password'])
            admin.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCreateStudentView(APIView):
    permission_classes = [permissions.IsAdminUser]

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


class AdminCreateTeacherView(APIView):
    permission_classes = [permissions.IsAdminUser]

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


class AdminStudentProfileView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, id):
        student = StudentProfile.objects.get(id=id)
        serializer = StudentProfileSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        student = StudentProfile.objects.get(id=id)
        serializer = StudentProfileSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        student = MyUser.objects.get(id=id)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class AdminTeacherProfileView(APIView):
    permission_classes = [permissions.IsAdminUser]

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


class AdminGroupCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['group_name', 'group_type', 'group_url', 'group_description', 'group_year', 'group_owner'],
            properties={
                'group_name': openapi.Schema(type=openapi.TYPE_STRING),
                'group_type': openapi.Schema(type=openapi.TYPE_STRING),
                'group_url': openapi.Schema(type=openapi.TYPE_STRING),
                'group_description': openapi.Schema(type=openapi.TYPE_STRING),
                'group_year': openapi.Schema(type=openapi.TYPE_STRING),
                'group_owner': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'OK', 400: 'Invalid Data'},
        operation_description="Update student profile"
    )
    def post(self, request):
        data = request.data
        group_owner_id = data.get('group_owner')
        try:
            group_owner = MyUser.objects.get(id=group_owner_id)
        except MyUser.DoesNotExist:
            return Response({'error': 'Invalid group owner id'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save(group_owner=group_owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminGroupDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, id):
        group = get_object_or_404(Group, id=id)
        serializer = GroupDetailSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        group = get_object_or_404(Group, id=id)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['group_name', 'group_type', 'group_url', 'group_description', 'group_year'],
            properties={
                'group_name': openapi.Schema(type=openapi.TYPE_STRING),
                'group_type': openapi.Schema(type=openapi.TYPE_STRING),
                'group_url': openapi.Schema(type=openapi.TYPE_STRING),
                'group_description': openapi.Schema(type=openapi.TYPE_STRING),
                'group_year': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'OK', 400: 'Invalid Data'},
        operation_description="Update student profile"
    )
    def patch(self, request, id):
        group = Group.objects.get(id=id)
        serializer = GroupDetailSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class AdminCreateEventView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['event_name', 'event_description', 'event_date', 'event_place', "event_status"],
            properties={
                "event_name": openapi.Schema(type=openapi.TYPE_STRING),
                "event_description": openapi.Schema(type=openapi.TYPE_STRING),
                "event_date": openapi.Schema(type=openapi.TYPE_STRING),
                "event_place": openapi.Schema(type=openapi.TYPE_STRING),
                "event_status": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
        ),
        responses={200: "OK", 400: "Invalid Data"},
        operation_description="Create Event"
    )
    def post(self, request):
        data = request.data
        event_owner_id = data.get('event_owner')
        try:
            event_owner = MyUser.objects.get(id=event_owner_id)
        except MyUser.DoesNotExist:
            return Response({'error': 'Invalid group owner id'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save(event_owner=event_owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminEventDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, id):
        event = Event.objects.get(id=id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['event_name', 'event_description', 'event_date', 'event_place', "event_status"],
            properties={
                "event_name": openapi.Schema(type=openapi.TYPE_STRING),
                "event_description": openapi.Schema(type=openapi.TYPE_STRING),
                "event_date": openapi.Schema(type=openapi.TYPE_STRING),
                "event_place": openapi.Schema(type=openapi.TYPE_STRING),
                "event_status": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
        ),
        responses={200: "OK", 400: "Invalid Data"},
        operation_description="Event info update"
    )
    def patch(self, request, id):
        event = Event.objects.get(id=id)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # def delete(self, request, id):
        event = Event.objects.get(id=id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

