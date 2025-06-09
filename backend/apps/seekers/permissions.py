from rest_framework.permissions import BasePermission
from .models import SeekerProfile

class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list']:
            return True

        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.role in ['admin', 'job_seeker']

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True

        if isinstance(obj, SeekerProfile):
            return obj.user == request.user
        
        if hasattr(obj, 'seeker'):
            return obj.seeker.user == request.user

        return False