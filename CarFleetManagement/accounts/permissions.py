from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'is_admin', False)

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'is_manager', False)

class IsCoordinator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'is_coordinator', False)

class IsDriver(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'is_driver', False)

class IsTestUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'is_testuser', False)

class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, 'is_admin', False) or getattr(request.user, 'is_manager', False)
        )


class ScopedPermission(permissions.BasePermission):
    """
    Check if the user's role has the required permission for the current resource.
    Requires 'required_scope' to be set on the view.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        required_scope = getattr(view, 'required_scope', None)
        if not required_scope:
            return True  # Fallback to IsAuthenticated if no scope defined

        role = getattr(request.user, 'role', None)
        if not role:
            return False

        # Map DRF actions or HTTP methods to scope actions
        action_map = {
            'list': 'read',
            'retrieve': 'read',
            'create': 'create',
            'update': 'update',
            'partial_update': 'update',
            'destroy': 'delete',
        }

        action = None
        if hasattr(view, 'action'):
            action = action_map.get(view.action)

        if not action:
            method_to_action = {
                'GET': 'read',
                'POST': 'create',
                'PUT': 'update',
                'PATCH': 'update',
                'DELETE': 'delete',
            }
            action = method_to_action.get(request.method)

        if not action:
            return False

        role_permissions = getattr(role, 'permissions', {})
        resource_perms = role_permissions.get(required_scope, [])

        return action in resource_perms
