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
        
        # Create roles
        self.admin_role = UserRole.objects.create(name='ADMIN', description='Admin')
        self.manager_role = UserRole.objects.create(name='MANAGER', description='Manager')
        self.coordinator_role = UserRole.objects.create(name='COORDINATOR', description='Coordinator')
        self.driver_role = UserRole.objects.create(name='DRIVER', description='Driver')
        self.testuser_role = UserRole.objects.create(name='TESTUSER', description='Test User')
        
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin', email='admin@test.com', password='pass', role=self.admin_role
        )
        self.manager_user = User.objects.create_user(
            username='manager', email='manager@test.com', password='pass', role=self.manager_role
        )
        self.coordinator_user = User.objects.create_user(
            username='coordinator', email='coordinator@test.com', password='pass', role=self.coordinator_role
        )
        self.driver_user = User.objects.create_user(
            username='driver', email='driver@test.com', password='pass', role=self.driver_role
        )
        self.testuser_user = User.objects.create_user(
            username='testuser', email='testuser@test.com', password='pass', role=self.testuser_role
        )
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