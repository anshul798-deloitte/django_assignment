from typing import Type

from django.http.request import HttpRequest
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_admin and request.user.is_authenticated

class IsManager(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_manager and request.user.is_authenticated

class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_admin

