"""
Django management command to set up development test users.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from CarFleetManagement.accounts.models import UserRole

User = get_user_model()


class Command(BaseCommand):
    help = "Create development test users"

    def handle(self, *args, **options):
        """Create test users for development."""

        # Check if we're in development mode
        environment = os.environ.get("ENVIRONMENT", "development")
        if environment != "development":
            self.stdout.write(self.style.ERROR("❌ ERROR: This command should only be run in development mode!"))
            self.stdout.write(f"Current environment: {environment}")
            return

        self.stdout.write("🚀 Setting up development test credentials...")
        self.stdout.write("=" * 50)

        # Create or get user roles first
        admin_role, created = UserRole.objects.get_or_create(
            name=UserRole.ADMIN, defaults={"description": "Administrator with full system access"}
        )
        driver_role, created = UserRole.objects.get_or_create(
            name=UserRole.DRIVER, defaults={"description": "Driver with limited access"}
        )

        self.stdout.write("✅ User roles created/verified")

        # Admin user credentials from environment
        admin_username = os.environ.get("DEV_ADMIN_USERNAME", "admin")
        admin_email = os.environ.get("DEV_ADMIN_EMAIL", "admin@fleetmanagement.dev")
        admin_password = os.environ.get("DEV_ADMIN_PASSWORD", "admin123!")

        # Regular user credentials from environment
        user_username = os.environ.get("DEV_USER_USERNAME", "testuser")
        user_email = os.environ.get("DEV_USER_EMAIL", "user@fleetmanagement.dev")
        user_password = os.environ.get("DEV_USER_PASSWORD", "user123!")

        # Create or update admin user
        admin_user, created = User.objects.get_or_create(
            username=admin_username,
            defaults={
                "email": admin_email,
                "is_staff": True,
                "is_superuser": True,
                "first_name": "Admin",
                "last_name": "User",
                "role": admin_role,
            },
        )

        if created:
            admin_user.set_password(admin_password)
            admin_user.save()
            self.stdout.write(f"✅ Created admin user: {admin_username}")
        else:
            # Update password in case it changed
            admin_user.set_password(admin_password)
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.role = admin_role
            admin_user.save()
            self.stdout.write(f"✅ Updated admin user: {admin_username}")

        # Create or update regular user
        regular_user, created = User.objects.get_or_create(
            username=user_username,
            defaults={
                "email": user_email,
                "is_staff": False,
                "is_superuser": False,
                "first_name": "Test",
                "last_name": "User",
                "role": driver_role,
            },
        )

        if created:
            regular_user.set_password(user_password)
            regular_user.save()
            self.stdout.write(f"✅ Created regular user: {user_username}")
        else:
            # Update password in case it changed
            regular_user.set_password(user_password)
            regular_user.role = driver_role
            regular_user.save()
            self.stdout.write(f"✅ Updated regular user: {user_username}")

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("🎉 Development credentials setup complete!")
        self.stdout.write("\n📋 TEST CREDENTIALS:")
        self.stdout.write("   Admin User:")
        self.stdout.write(f"   - Username: {admin_username}")
        self.stdout.write(f"   - Password: {admin_password}")
        self.stdout.write(f"   - Email: {admin_email}")
        self.stdout.write("   - Role: Admin (full access)")
        self.stdout.write("")
        self.stdout.write("   Regular User:")
        self.stdout.write(f"   - Username: {user_username}")
        self.stdout.write(f"   - Password: {user_password}")
        self.stdout.write(f"   - Email: {user_email}")
        self.stdout.write("   - Role: Driver (limited access)")
        self.stdout.write("\n🌐 Access URLs:")
        self.stdout.write("   - Login: http://localhost:8000/accounts/login/")
        self.stdout.write("   - Register: http://localhost:8000/accounts/register/")
        self.stdout.write("   - Admin: http://localhost:8000/admin/")
        self.stdout.write("   - API: http://localhost:8000/api/")
        self.stdout.write("\n⚠️  WARNING: These are development credentials only!")
        self.stdout.write("   DO NOT use these in production!")

        self.stdout.write(self.style.SUCCESS("\n✅ Setup completed successfully!"))
