"""
Tests for accounts permissions.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from CarFleetManagement.accounts.permissions import (
    IsAdmin, IsManager, IsCoordinator, IsDriver, IsTestUser, IsAdminOrManager
)
from CarFleetManagement.accounts.models import UserRole

User = get_user_model()


class PermissionsTestCase(TestCase):
    """Test cases for custom permissions."""

    def setUp(self):
        """Set up test data."""
        self.factory = APIRequestFactory()
        # Create roles (idempotent)
        self.admin_role, _ = UserRole.objects.get_or_create(
            name=UserRole.ADMIN, defaults={'description': 'Admin'}
        )
        self.manager_role, _ = UserRole.objects.get_or_create(
            name=UserRole.MANAGER, defaults={'description': 'Manager'}
        )
        self.coordinator_role, _ = UserRole.objects.get_or_create(
            name=UserRole.COORDINATOR, defaults={'description': 'Coordinator'}
        )
        self.driver_role, _ = UserRole.objects.get_or_create(
            name=UserRole.DRIVER, defaults={'description': 'Driver'}
        )
        self.testuser_role, _ = UserRole.objects.get_or_create(
            name=UserRole.TESTUSER, defaults={'description': 'Test User'}
        )

        # Create users (idempotent)
        self.admin_user, _ = User.objects.get_or_create(
            username='admin', defaults={'email': 'admin@test.com', 'role': self.admin_role}
        )
        self.admin_user.set_password('pass')
        self.admin_user.role = self.admin_role
        self.admin_user.save()

        self.manager_user, _ = User.objects.get_or_create(
            username='manager', defaults={'email': 'manager@test.com', 'role': self.manager_role}
        )
        self.manager_user.set_password('pass')
        self.manager_user.role = self.manager_role
        self.manager_user.save()

        self.coordinator_user, _ = User.objects.get_or_create(
            username='coordinator', defaults={'email': 'coordinator@test.com', 'role': self.coordinator_role}
        )
        self.coordinator_user.set_password('pass')
        self.coordinator_user.role = self.coordinator_role
        self.coordinator_user.save()

        self.driver_user, _ = User.objects.get_or_create(
            username='driver', defaults={'email': 'driver@test.com', 'role': self.driver_role}
        )
        self.driver_user.set_password('pass')
        self.driver_user.role = self.driver_role
        self.driver_user.save()

        self.testuser_user, _ = User.objects.get_or_create(
            username='testuser', defaults={'email': 'testuser@test.com', 'role': self.testuser_role}
        )
        self.testuser_user.set_password('pass')
        self.testuser_user.role = self.testuser_role
        self.testuser_user.save()
        self.anonymous_user = User()  # Anonymous user

    def test_is_admin_permission(self):
        """Test IsAdmin permission."""
        permission = IsAdmin()
        
        # Test with admin user
        request = self.factory.get('/')
        request.user = self.admin_user
        self.assertTrue(permission.has_permission(request, None))
        
        # Test with non-admin user
        request.user = self.driver_user
        self.assertFalse(permission.has_permission(request, None))
        
        # Test with anonymous user
        request.user = self.anonymous_user
        self.assertFalse(permission.has_permission(request, None))

    def test_is_manager_permission(self):
        """Test IsManager permission."""
        permission = IsManager()
        
        # Test with manager user
        request = self.factory.get('/')
        request.user = self.manager_user
        self.assertTrue(permission.has_permission(request, None))
        
        # Test with non-manager user
        request.user = self.driver_user
        self.assertFalse(permission.has_permission(request, None))
        
        # Test with anonymous user
        request.user = self.anonymous_user
        self.assertFalse(permission.has_permission(request, None))

    def test_is_coordinator_permission(self):
        """Test IsCoordinator permission."""
        permission = IsCoordinator()
        
        # Test with coordinator user
        request = self.factory.get('/')
        request.user = self.coordinator_user
        self.assertTrue(permission.has_permission(request, None))
        
        # Test with non-coordinator user
        request.user = self.driver_user
        self.assertFalse(permission.has_permission(request, None))
        
        # Test with anonymous user
        request.user = self.anonymous_user
        self.assertFalse(permission.has_permission(request, None))

    def test_is_driver_permission(self):
        """Test IsDriver permission."""
        permission = IsDriver()
        
        # Test with driver user
        request = self.factory.get('/')
        request.user = self.driver_user
        self.assertTrue(permission.has_permission(request, None))
        
        # Test with non-driver user
        request.user = self.admin_user
        self.assertFalse(permission.has_permission(request, None))
        
        # Test with anonymous user
        request.user = self.anonymous_user
        self.assertFalse(permission.has_permission(request, None))

    def test_is_testuser_permission(self):
        """Test IsTestUser permission."""
        permission = IsTestUser()
        
        # Test with testuser user
        request = self.factory.get('/')
        request.user = self.testuser_user
        self.assertTrue(permission.has_permission(request, None))
        
        # Test with non-testuser user
        request.user = self.driver_user
        self.assertFalse(permission.has_permission(request, None))
        
        # Test with anonymous user
        request.user = self.anonymous_user
        self.assertFalse(permission.has_permission(request, None))

    def test_is_admin_or_manager_permission(self):
        """Test IsAdminOrManager permission."""
        permission = IsAdminOrManager()
        
        # Test with admin user
        request = self.factory.get('/')
        request.user = self.admin_user
        self.assertTrue(permission.has_permission(request, None))
        
        # Test with manager user
        request.user = self.manager_user
        self.assertTrue(permission.has_permission(request, None))
        
        # Test with coordinator user (should fail)
        request.user = self.coordinator_user
        self.assertFalse(permission.has_permission(request, None))
        
        # Test with driver user (should fail)
        request.user = self.driver_user
        self.assertFalse(permission.has_permission(request, None))
        
        # Test with anonymous user
        request.user = self.anonymous_user
        self.assertFalse(permission.has_permission(request, None))

    def test_permissions_with_missing_attributes(self):
        """Test permissions when user doesn't have role attributes."""
        # Create a user without role attributes
        user_without_role = User.objects.create_user(
            username='norole', email='norole@test.com', password='pass'
        )
        
        request = self.factory.get('/')
        request.user = user_without_role
        
        # All permissions should return False for users without proper role attributes
        self.assertFalse(IsAdmin().has_permission(request, None))
        self.assertFalse(IsManager().has_permission(request, None))
        self.assertFalse(IsCoordinator().has_permission(request, None))
        self.assertFalse(IsDriver().has_permission(request, None))
        self.assertFalse(IsTestUser().has_permission(request, None))
        self.assertFalse(IsAdminOrManager().has_permission(request, None))