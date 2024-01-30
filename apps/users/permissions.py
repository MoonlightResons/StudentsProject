from rest_framework import permissions


class AnnonPermission(permissions.BasePermission):
    message = 'You are arledy authenticated'

    def has_permission(self, request, view):
        return not request.user.is_authenticated