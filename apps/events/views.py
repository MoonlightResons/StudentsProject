from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import EventSerializer
from .models import Event
from ..users.models import MyUser
from apps.users.permissions import EventOwner


class CreateEventView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['group_name', 'group_description', 'group_date', 'group_place'],
            properties={
                "group_name": openapi.Schema(type=openapi.TYPE_STRING),
                "group_description": openapi.Schema(type=openapi.TYPE_STRING),
                "group_date": openapi.Schema(type=openapi.TYPE_STRING),
                "group_place": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: "OK", 400: "Invalid Data"},
        operation_description="Create Event"
    )
    def post(self, request):
        user = MyUser.objects.get(theuser=request.user)
        data = request.data
        data['event_owner'] = user.id
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    permission_classes = [EventOwner]

    def get(self, request, id):
        event = Event.objects.get(id=id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['group_name', 'group_description', 'group_date', 'group_place'],
            properties={
                "group_name": openapi.Schema(type=openapi.TYPE_STRING),
                "group_description": openapi.Schema(type=openapi.TYPE_STRING),
                "group_date": openapi.Schema(type=openapi.TYPE_STRING),
                "group_place": openapi.Schema(type=openapi.TYPE_STRING),
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

    def delete(self, request, id):
        event = Event.objects.get(id=id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
