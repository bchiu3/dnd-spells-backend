from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.conf import settings

class IsAuthenticatedOrNoLoginOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if settings.DATABASES is None or not 'default' in settings.DATABASES or settings.DATABASES['default']['HOST'] is None:
            return True
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )