from rest_framework.permissions import BasePermission


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
