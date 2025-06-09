from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Handles nested objects (e.g., job -> company -> user).
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `user`.
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Handle seeker profile related objects
        if hasattr(obj, 'seeker'):
            return obj.seeker.user == request.user
            
        # Handle company related objects (like jobs)
        if hasattr(obj, 'company'):
            return obj.company.user == request.user

        return False 