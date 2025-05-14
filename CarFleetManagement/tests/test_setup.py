"""
Test setup for the Car Fleet Management project.

This module contains setup functions and patches that should be applied
to all test files to ensure proper authentication and serialization.
"""
import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

# Configure Django settings before importing any models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.settings")

# Setup Django
django.setup()

# Now it's safe to import Django models
from django.conf import settings
from rest_framework import serializers
from accounts.models import CustomUser, UserRole
from tests.auth_utils import authenticate_client

# Custom UserSerializer for tests that works with CustomUser model
class TestUserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model for tests."""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']

def setup_test_environment():
    """
    Set up the test environment with all necessary patches and configurations.
    
    This function should be called at the beginning of each test file.
    """
    # Patch the UserSerializer in api.serializers
    import api.serializers
    api.serializers.UserSerializer = TestUserSerializer
    api.serializers.User = CustomUser
    
    # Patch permission classes for testing if needed
    # This can be uncommented if you want to relax permissions during tests
    # from rest_framework.permissions import IsAuthenticated, IsAdminUser
    # IsAdminUser.has_permission = lambda self, request, view: True
    
    return True  # Return True to indicate successful setup

def create_admin_user_with_staff():
    """Create an admin user with staff permissions for testing."""
    admin_role, _ = UserRole.objects.get_or_create(name=UserRole.ADMIN, description='Administrator role')
    admin_user = CustomUser.objects.create_user(
        username='admin_test',
        email='admin_test@example.com',
        password='password123',
        role=admin_role,
        is_staff=True  # Set is_staff to True for admin users to pass IsAdminUser permission
    )
    return admin_user

def get_authenticated_client(user=None):
    """Get an authenticated client for the given user."""
    if user is None:
        user = create_admin_user_with_staff()
    
    from rest_framework.test import APIClient
    client = APIClient()
    authenticate_client(client, user)
    return client, user


import pytest

@pytest.mark.django_db
def test_setup_environment():
    """Test that the setup_test_environment function works correctly."""
    # Call the setup function
    result = setup_test_environment()
    
    # Verify it returns True
    assert result is True
    
    # Verify the UserSerializer is patched
    import api.serializers
    assert api.serializers.UserSerializer == TestUserSerializer
    assert api.serializers.User == CustomUser

@pytest.mark.django_db
def test_get_authenticated_client():
    """Test that the get_authenticated_client function works correctly."""
    # Get an authenticated client
    client, user = get_authenticated_client()
    
    # Verify the user is an admin with staff permissions
    assert user.role.name == UserRole.ADMIN
    assert user.is_staff is True
    
    # Just verify that we got a client and user back
    assert client is not None
    assert user is not None
    assert user.username == 'admin_test'
