from rest_framework import permissions

class AnnonPermission(permissions.BasePermission):
    message = 'You are arledy authenticated'

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class ProfileOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.studentuser == request.user


class GroupOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.group_owner == request.user


class EventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.event_owner == request.user