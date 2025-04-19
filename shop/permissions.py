from rest_framework import permissions
from apps.accounts.models import Employer
class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user and request.user.is_authenticated:
            return Employer.objects.filter(user=request.user).exists()
        return False

    # def has_object_permission(self, request, view, obj):
    #     """
    #     Return `True` if permission is granted, `False` otherwise.
    #     """
    #     return True