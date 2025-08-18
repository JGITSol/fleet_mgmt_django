from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

class JWTAuthTestMixin:
    """
    Mixin to provide JWT authentication and user creation utilities for DRF API tests.
    """
    def create_user_with_role(self, username, password, role_name, is_staff=False, is_superuser=False):
        User = get_user_model()
        # Pass is_staff and is_superuser to create_user
        user = User.objects.create_user(username=username, password=password, is_staff=is_staff, is_superuser=is_superuser)
        # Assign role if roles are used
        if hasattr(user, 'role'):
            from CarFleetManagement.accounts.models import UserRole
            role, _ = UserRole.objects.get_or_create(name=role_name)
            user.role = role
            user.save() # Save again to persist role and any other changes from create_user
        return user

    def authenticate_client(self, user=None, role_name='ADMIN', is_staff=None, is_superuser=None):
        """
        Create (if needed) and authenticate self.client with a JWT token for the given user/role.
        Allows specifying is_staff and is_superuser, defaulting to True for ADMIN role.
        """
        if not hasattr(self, 'client'):
            from rest_framework.test import APIClient
            self.client = APIClient()
        
        if user is None:
            username = f'testuser_{role_name.lower()}'
            password = 'testpass123'
            
            # Determine staff/superuser status
            # Default to True for ADMIN if not explicitly provided
            final_is_staff = is_staff if is_staff is not None else (role_name == 'ADMIN')
            final_is_superuser = is_superuser if is_superuser is not None else (role_name == 'ADMIN')
            
            user = self.create_user_with_role(
                username,
                password,
                role_name,
                is_staff=final_is_staff,
                is_superuser=final_is_superuser
            )
            
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        return user
