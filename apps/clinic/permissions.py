from rest_framework import permissions


class IsClinicAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and (
                request.user.role == "clinic_admin"
                or request.user.is_superuser
            )
        )

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        return obj.clinic.clinic_admin == request.user