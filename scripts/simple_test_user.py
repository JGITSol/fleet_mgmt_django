#!/usr/bin/env python3
"""
Simple test user setup without permissions field
"""

import os
import sys
from pathlib import Path

# Add Django project to Python path
project_root = Path(__file__).parent / "CarFleetManagement"
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.settings")

import django


def setup_simple_test_user():
    """Setup test user with admin role (without permissions field)"""

    # Ensure Django is configured when this script runs (avoids module-level side-effects)
    django.setup()

    from django.contrib.auth import get_user_model
    from CarFleetManagement.accounts.models import UserRole

    User = get_user_model()


    print("🔧 Setting up simple test user")
    print("=" * 50)

    # Create or get admin role (without permissions)
    admin_role, created = UserRole.objects.get_or_create(
        name=UserRole.ADMIN,
        defaults={"description": "Administrator with full system access"},
    )

    if created:
        print("✓ Created admin role")
    else:
        print("✓ Admin role already exists")

    # Create or update test user
    try:
        test_user = User.objects.get(username="testuser")
        test_user.role = admin_role
        test_user.is_staff = True
        test_user.is_superuser = True
        test_user.save()
        print("✓ Updated existing test user with admin role")
    except User.DoesNotExist:
        test_user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
                password=__import__('conftest').TEST_PASSWORD,
            first_name="Test",
            last_name="User",
            role=admin_role,
            is_staff=True,
            is_superuser=True,
        )
        print("✓ Created new test user with admin role")

    print(f"\n📊 Test User: {test_user.username}")
    print(f"   Role: {test_user.role.name if test_user.role else 'None'}")
    print(f"   Staff: {test_user.is_staff}")
    print(f"   Superuser: {test_user.is_superuser}")

    return test_user


if __name__ == "__main__":
    # When executed as a script, ensure Django is initialized before running
    # the setup logic. The function itself calls django.setup() as well, so
    # this is defensive but safe to keep.
    setup_simple_test_user()
