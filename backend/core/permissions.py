from rest_framework import permissions

class IsAdminUserCustom(permissions.BasePermission):
    """
    Allows access only to super users (super_usuario == 'S' or '1').
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.super_usuario in ['S', '1', 's']))
