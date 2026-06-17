"""User permissions."""
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class IsAdmin(BasePermission):
    """Permission for admin users only."""
    
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated and request.user.is_admin


class IsManager(BasePermission):
    """Permission for manager and admin users."""
    
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_manager)


class IsOwnerOrAdmin(BasePermission):
    """Permission for owner or admin."""
    
    def has_object_permission(self, request: Request, view: View, obj) -> bool:
        return request.user.is_authenticated and (obj == request.user or request.user.is_admin)
