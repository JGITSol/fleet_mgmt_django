"""
Test setup for the Car Fleet Management project.

This module contains setup functions and patches that should be applied
to all test files to ensure proper authentication and serialization.
"""

import os
from typing import ClassVar

from rest_framework import serializers

# Defer Django setup and model imports to runtime to avoid module-level
# side-effects and E402 lint warnings. Test runtime (pytest-django) will
# provide the proper environment when fixtures/functions call django.setup().
from tests.auth_utils import authenticate_client

# Make CustomUser/UserRole visible to static analyzers (Ruff/pyright) while
# keeping runtime behavior intact. If models can be imported now (test run
# environment), use them; otherwise fall back to Any for lint-time.
try:
    from CarFleetManagement.accounts.models import CustomUser, UserRole  # type: ignore[attr-defined]
except Exception:  # pragma: no cover - lint-time fallback
    from typing import Any

    CustomUser = Any  # type: ignore[assignment]
    UserRole = Any  # type: ignore[assignment]

_TEST_PASSWORD = os.environ.get("TEST_PASSWORD", "password123")

def _get_models():
    import django

    django.setup()
    from CarFleetManagement.accounts.models import CustomUser, UserRole

    return CustomUser, UserRole


# Custom UserSerializer for tests that works with CustomUser model
class AppTestUserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model for tests."""

    class Meta:
        model = CustomUser
        # Ensure DRF reads these from Meta (not as a class attribute on the
        # serializer itself). Declaring them at the serializer class level
        # used to set `fields` to a plain list which broke DRF's internals
        # (it expects a mapping-like `self.fields`).
        fields: ClassVar[list[str]] = ["id", "username", "email", "first_name", "last_name", "role"]
        read_only_fields: ClassVar[list[str]] = ["id"]


def setup_test_environment():
    """
    Set up the test environment with all necessary patches and configurations.

    This function should be called at the beginning of each test file.
    """
    # Patch the UserSerializer in api.serializers
    import api.serializers

    api.serializers.UserSerializer = AppTestUserSerializer
    api.serializers.User = CustomUser

    # Patch permission classes for testing if needed
    # This can be uncommented if you want to relax permissions during tests
    # from rest_framework.permissions import IsAuthenticated, IsAdminUser
    # IsAdminUser.has_permission = lambda self, request, view: True

    return True  # Return True to indicate successful setup


def create_admin_user_with_staff():
    """Create an admin user with staff permissions for testing."""
    CustomUser, UserRole = _get_models()
    admin_role, _ = UserRole.objects.get_or_create(name=UserRole.ADMIN, defaults={"description": "Administrator role"})
    admin_user = CustomUser.objects.create_user(
        username="admin_test",
        email="admin_test@example.com",
        password=_TEST_PASSWORD,
        role=admin_role,
        is_staff=True,  # Set is_staff to True for admin users to pass IsAdminUser permission
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

    # Verify the UserSerializer is patched (guarded to satisfy static analysis)
    import api.serializers

    if hasattr(api.serializers, "UserSerializer"):
        assert api.serializers.UserSerializer == AppTestUserSerializer
    if hasattr(api.serializers, "User"):
        assert api.serializers.User == CustomUser


@pytest.mark.django_db
def test_get_authenticated_client():
    """Test that the get_authenticated_client function works correctly."""
    # Get an authenticated client
    client, user = get_authenticated_client()

    # Verify the user is an admin with staff permissions
    if hasattr(user, "role") and getattr(user.role, "name", None) is not None:
        assert user.role.name == UserRole.ADMIN
    assert user.is_staff is True

    # Just verify that we got a client and user back
    assert client is not None
    assert user is not None
    assert user.username == "admin_test"
