#!/usr/bin/env python
"""
Development Credentials Setup Script
====================================

This script creates test users for development purposes.
DO NOT run this in production!

Creates:
- Admin user: admin / admin123!
- Regular user: testuser / user123!
"""

import os
import sys
import django
from pathlib import Path
from dotenv import load_dotenv

# Add the CarFleetManagement directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'CarFleetManagement'))

# Load environment variables first
load_dotenv(Path(__file__).parent / 'CarFleetManagement' / '.env')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import UserRole

User = get_user_model()

def create_test_users():
    """Create test users for development."""
    
    # Check if we're in development mode
    environment = os.environ.get('ENVIRONMENT', 'development')
    if environment != 'development':
        print("❌ ERROR: This script should only be run in development mode!")
        print(f"Current environment: {environment}")
        return False
    
    print("🚀 Setting up development test credentials...")
    print("=" * 50)
    
    # Create or get user roles first
    admin_role, _ = UserRole.objects.get_or_create(
        name=UserRole.ADMIN,
        defaults={'description': 'Administrator with full system access'}
    )
    driver_role, _ = UserRole.objects.get_or_create(
        name=UserRole.DRIVER,
        defaults={'description': 'Driver with limited access'}
    )
    
    print("✅ User roles created/verified")
    
    # Admin user credentials from environment
    admin_username = os.environ.get('DEV_ADMIN_USERNAME', 'admin')
    admin_email = os.environ.get('DEV_ADMIN_EMAIL', 'admin@fleetmanagement.dev')
    admin_password = os.environ.get('DEV_ADMIN_PASSWORD', 'admin123!')
    
    # Regular user credentials from environment
    user_username = os.environ.get('DEV_USER_USERNAME', 'testuser')
    user_email = os.environ.get('DEV_USER_EMAIL', 'user@fleetmanagement.dev')
    user_password = os.environ.get('DEV_USER_PASSWORD', 'user123!')
    
    # Create or update admin user
    admin_user, created = User.objects.get_or_create(
        username=admin_username,
        defaults={
            'email': admin_email,
            'is_staff': True,
            'is_superuser': True,
            'first_name': 'Admin',
            'last_name': 'User',
            'role': admin_role
        }
    )
    
    if created:
        admin_user.set_password(admin_password)
        admin_user.save()
        print(f"✅ Created admin user: {admin_username}")
    else:
        # Update password in case it changed
        admin_user.set_password(admin_password)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.role = admin_role
        admin_user.save()
        print(f"✅ Updated admin user: {admin_username}")
    
    # Create or update regular user
    regular_user, created = User.objects.get_or_create(
        username=user_username,
        defaults={
            'email': user_email,
            'is_staff': False,
            'is_superuser': False,
            'first_name': 'Test',
            'last_name': 'User',
            'role': driver_role
        }
    )
    
    if created:
        regular_user.set_password(user_password)
        regular_user.save()
        print(f"✅ Created regular user: {user_username}")
    else:
        # Update password in case it changed
        regular_user.set_password(user_password)
        regular_user.role = driver_role
        regular_user.save()
        print(f"✅ Updated regular user: {user_username}")
    
    print("\n" + "=" * 50)
    print("🎉 Development credentials setup complete!")
    print("\n📋 TEST CREDENTIALS:")
    print(f"   Admin User:")
    print(f"   - Username: {admin_username}")
    print(f"   - Password: {admin_password}")
    print(f"   - Email: {admin_email}")
    print(f"   - Role: Admin (full access)")
    print()
    print(f"   Regular User:")
    print(f"   - Username: {user_username}")
    print(f"   - Password: {user_password}")
    print(f"   - Email: {user_email}")
    print(f"   - Role: Driver (limited access)")
    print("\n🌐 Access URLs:")
    print("   - Login: http://localhost:8000/accounts/login/")
    print("   - Register: http://localhost:8000/accounts/register/")
    print("   - Admin: http://localhost:8000/admin/")
    print("   - API: http://localhost:8000/api/")
    print("\n⚠️  WARNING: These are development credentials only!")
    print("   DO NOT use these in production!")
    
    return True

def main():
    """Main function."""
    try:
        success = create_test_users()
        if success:
            print("\n✅ Setup completed successfully!")
        else:
            print("\n❌ Setup failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()