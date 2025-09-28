"""
Authentication test mixin for the Car Fleet Management project.
"""

from conftest import TEST_PASSWORD
from rest_framework.test import APIClient

from CarFleetManagement.accounts.models import CustomUser, UserRole
from tests.auth_utils import authenticate_client


class AuthTestMixin:
    """
    Mixin for authentication in test cases.

    This mixin provides helper methods for creating users with different roles
    and authenticating test clients.
    """

    def create_admin_user(self):
        """Create an admin user for testing."""
        admin_role, _ = UserRole.objects.get_or_create(name=UserRole.ADMIN, description="Administrator role")
        admin_user = CustomUser.objects.create_user(
            username="admin_test",
            email="admin_test@example.com",
            password=TEST_PASSWORD,
            role=admin_role,
            is_staff=True,  # Set is_staff to True for admin users to pass IsAdminUser permission
        )
        return admin_user

    def create_driver_user(self):
        """Create a driver user for testing."""
        driver_role, _ = UserRole.objects.get_or_create(name=UserRole.DRIVER, description="Driver role")
        driver_user = CustomUser.objects.create_user(
            username="driver_test", email="driver_test@example.com", password=TEST_PASSWORD, role=driver_role
        )
        return driver_user

    def create_maintenance_user(self):
        """Create a maintenance user for testing."""
        maintenance_role, _ = UserRole.objects.get_or_create(name=UserRole.MAINTENANCE, description="Maintenance role")
        maintenance_user = CustomUser.objects.create_user(
            username="maintenance_test",
            email="maintenance_test@example.com",
            password=TEST_PASSWORD,
            role=maintenance_role,
        )
        return maintenance_user

    def get_authenticated_client(self, user=None):
        """Get an authenticated client for the given user."""
        if user is None:
            user = self.create_admin_user()

        client = APIClient()
        authenticate_client(client, user)
        return client, user
