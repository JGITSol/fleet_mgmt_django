from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

class JWTAuthTestMixin:
    """
    Mixin to provide JWT authentication and user creation utilities for DRF API tests.
    """
    def create_user_with_role(self, username, password, role_name):
        User = get_user_model()
        user = User.objects.create_user(username=username, password=password)
        # Assign role if roles are used
        if hasattr(user, 'role'):
            from accounts.models import UserRole
            role, _ = UserRole.objects.get_or_create(name=role_name)
            user.role = role
            user.save()
        return user

    def authenticate_client(self, user=None, role_name='ADMIN'):
        """
        Create (if needed) and authenticate self.client with a JWT token for the given user/role.
        """
        if not hasattr(self, 'client'):
            from rest_framework.test import APIClient
            self.client = APIClient()
        if user is None:
            username = f'testuser_{role_name.lower()}'
            password = 'testpass123'
            user = self.create_user_with_role(username, password, role_name)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        return user
