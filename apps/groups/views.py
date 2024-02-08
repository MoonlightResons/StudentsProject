from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import GroupSerializer, GroupRequestSerializer, GroupDetailSerializer
from .models import Group
from apps.users.permissions import GroupOwner
from django.shortcuts import get_object_or_404
from apps.users.models import MyUser
from drf_yasg import openapi


class GroupCreateView(APIView):

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
    def post(self, request):
        user = MyUser.objects.get(theuser=request.user)
        data = request.data
        data['group_owner'] = user.id
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailView(APIView):
    permission_classes = [GroupOwner]

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

    def get(self, request, id):
        group = get_object_or_404(Group, id=id)
        serializer = GroupDetailSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        group = get_object_or_404(Group, id=id)

        # if request.user != team.team_owner:
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, id):
        group = Group.objects.get(id=id)
        serializer = GroupDetailSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class GroupMemberRequestVIew(APIView):

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

    def get(self, request, id):
        group = get_object_or_404(Group, id=id)
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        user = MyUser.objects.get(theuser=request.user)
        group = get_object_or_404(Group, id=id)

        if user not in group.group_member.all():
            group.group_member.add(user)
        else:
            return Response({"detail": "Пользователь уже является членом группы"}, status=status.HTTP_400_BAD_REQUEST)

        group.save()

        serializer = GroupRequestSerializer(group, data={}, partial=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = MyUser.objects.get(theuser=request.user)
        group = get_object_or_404(Group, id=id)

        if group.group_member.filter(id=user.id).exists():
            group.group_member.remove(user)
            group.save()

            serializer = GroupRequestSerializer(group, data={}, partial=True)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Пользователь не является членом группы"}, status=status.HTTP_400_BAD_REQUEST)

