from rest_framework.permissions import BasePermission


class IsCompanyOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list']:
            return True

        if view.action in ['create', 'update', 'partial_update']:
            return request.user.role in ['admin', 'company']

        return False


class IsCompany(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "company"


class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.role == 'admin':
            return True

        if user.role == 'company':
            if view.action in ['retrieve', 'list', 'partial_update']:
                return True

        if user.role == 'job_seeker':
            if view.action in ['create', 'destroy', 'retrieve', 'list']:
                return True

        return False


class IsAdminOrJobOwner(BasePermission):
    """
    Allows access only to admin users or to the company user who owns the job.
    """
    def has_object_permission(self, request, view, obj):
        # Admins have full access.
        if request.user.is_staff or request.user.role == 'admin':
            return True
        
        # Write permissions are only allowed to the company that owns the job.
        return obj.company.user == request.user


class IsAdminOrApplicationOwnerOrCompany(BasePermission):
    """
    Allows access based on role:
    - Admin: Full access.
    - Seeker: Can view/delete their own applications.
    - Company: Can view/update applications for their own jobs.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.role == 'admin':
            return True
        
        if request.user.role == 'job_seeker':
            # Seekers can only access their own applications.
            return obj.applicant.user == request.user

        if request.user.role == 'company':
            # Companies can only access applications for jobs they own.
            return obj.job.company.user == request.user
            
        return False
