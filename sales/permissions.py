from rest_framework.permissions import BasePermission

class IsSalesOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'sales']