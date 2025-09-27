#!/usr/bin/env python3
"""
Setup test user with proper permissions
"""

import os
import sys
from pathlib import Path

# Add Django project to Python path
project_root = Path(__file__).parent / "CarFleetManagement"
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from CarFleetManagement.accounts.models import UserRole

User = get_user_model()

def setup_test_user():
    """Setup test user with admin role"""
    print("🔧 Setting up test user with admin permissions")
    print("=" * 50)
    
    # Create or get admin role
    admin_role, created = UserRole.objects.get_or_create(
        name=UserRole.ADMIN,
        defaults={
            'description': 'Administrator with full system access',
            'permissions': {'all': True}
        }
    )
    
    if created:
        print("✓ Created admin role")
    else:
        print("✓ Admin role already exists")
    
    # Create or update test user
    try:
        test_user = User.objects.get(username='testuser')
        test_user.role = admin_role
        test_user.is_staff = True
        test_user.is_superuser = True
        test_user.save()
        print("✓ Updated existing test user with admin role")
    except User.DoesNotExist:
        test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role=admin_role,
            is_staff=True,
            is_superuser=True
        )
        print("✓ Created new test user with admin role")
    
    # Create manager role for additional testing
    manager_role, created = UserRole.objects.get_or_create(
        name=UserRole.MANAGER,
        defaults={
            'description': 'Manager with fleet management access',
            'permissions': {'vehicles': True, 'drivers': True, 'maintenance': True}
        }
    )
    
    if created:
        print("✓ Created manager role")
    
    # Create test manager user
    try:
        manager_user = User.objects.get(username='manager')
        manager_user.role = manager_role
        manager_user.save()
        print("✓ Updated existing manager user")
    except User.DoesNotExist:
        manager_user = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='manager123',
            first_name='Test',
            last_name='Manager',
            role=manager_role
        )
        print("✓ Created new manager user")
    
    print("\n📊 User Summary:")
    print(f"  Admin User: {test_user.username} (Role: {test_user.role.name if test_user.role else 'None'})")
    print(f"  Manager User: {manager_user.username} (Role: {manager_user.role.name if manager_user.role else 'None'})")
    
    return test_user, manager_user

if __name__ == "__main__":
    setup_test_user()