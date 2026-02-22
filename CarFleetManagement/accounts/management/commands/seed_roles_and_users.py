"""
Django management command to seed all roles with industry-standard scopes
and create demo users for each role.

Idempotent — safe to run repeatedly. Existing users/roles are updated.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from CarFleetManagement.accounts.models import CustomUser, UserRole, Driver

User = get_user_model()

# Industry-standard scope definitions per role.
# Keys are resource names, values are lists of allowed actions.
ROLE_SCOPES = {
    UserRole.ADMIN: {
        "vehicles": ["create", "read", "update", "delete"],
        "drivers": ["create", "read", "update", "delete"],
        "maintenance": ["create", "read", "update", "delete"],
        "emergencies": ["create", "read", "update", "delete"],
        "media": ["create", "read", "update", "delete"],
        "users": ["create", "read", "update", "delete"],
    },
    UserRole.MANAGER: {
        "vehicles": ["create", "read", "update", "delete"],
        "drivers": ["create", "read", "update", "delete"],
        "maintenance": ["create", "read", "update", "delete"],
        "emergencies": ["create", "read", "update"],
        "media": ["create", "read", "update", "delete"],
        "users": ["read"],
    },
    UserRole.COORDINATOR: {
        "vehicles": ["read"],
        "drivers": ["read", "update"],
        "maintenance": ["create", "read", "update"],
        "emergencies": ["create", "read", "update"],
        "media": ["create", "read"],
        "users": [],
    },
    UserRole.DRIVER: {
        "vehicles": ["read"],
        "drivers": ["read"],
        "maintenance": ["read"],
        "emergencies": ["create", "read"],
        "media": ["read"],
        "users": [],
    },
    UserRole.MAINTENANCE_STAFF: {
        "vehicles": ["read"],
        "drivers": [],
        "maintenance": ["create", "read", "update", "delete"],
        "emergencies": ["read"],
        "media": ["create", "read"],
        "users": [],
    },
    UserRole.TESTUSER: {
        "vehicles": ["create", "read", "update", "delete"],
        "drivers": ["create", "read", "update", "delete"],
        "maintenance": ["create", "read", "update", "delete"],
        "emergencies": ["create", "read", "update", "delete"],
        "media": ["create", "read", "update", "delete"],
        "users": ["read"],
    },
}

ROLE_DESCRIPTIONS = {
    UserRole.ADMIN: "Administrator with full system access",
    UserRole.MANAGER: "Fleet manager — full CRUD on fleet assets, read-only users",
    UserRole.COORDINATOR: "Operations coordinator — schedules maintenance, manages emergencies",
    UserRole.DRIVER: "Fleet driver — view-only access, can report emergencies",
    UserRole.MAINTENANCE_STAFF: "Maintenance technician — full maintenance CRUD, read vehicles",
    UserRole.TESTUSER: "Test account — full access for QA and demos",
}

DEMO_USERS = [
    {
        "username": "demo_admin",
        "email": "admin@fleet.dev",
        "first_name": "Admin",
        "last_name": "Demo",
        "role_name": UserRole.ADMIN,
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "username": "demo_manager",
        "email": "manager@fleet.dev",
        "first_name": "Maria",
        "last_name": "Kowalska",
        "role_name": UserRole.MANAGER,
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "demo_coordinator",
        "email": "coordinator@fleet.dev",
        "first_name": "Tomasz",
        "last_name": "Nowak",
        "role_name": UserRole.COORDINATOR,
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "demo_driver",
        "email": "driver@fleet.dev",
        "first_name": "Jan",
        "last_name": "Kierowca",
        "role_name": UserRole.DRIVER,
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "demo_maintenance",
        "email": "maintenance@fleet.dev",
        "first_name": "Piotr",
        "last_name": "Mechanik",
        "role_name": UserRole.MAINTENANCE_STAFF,
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "demo_tester",
        "email": "tester@fleet.dev",
        "first_name": "Test",
        "last_name": "Account",
        "role_name": UserRole.TESTUSER,
        "is_staff": False,
        "is_superuser": False,
    },
]

DEFAULT_PASSWORD = "fleet2026!"


class Command(BaseCommand):
    help = "Seed all roles with scoped permissions and create demo users for each role."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Seeding roles and demo users..."))

        # --- Upsert roles ---
        roles = {}
        for role_name, scopes in ROLE_SCOPES.items():
            role, created = UserRole.objects.update_or_create(
                name=role_name,
                defaults={
                    "description": ROLE_DESCRIPTIONS.get(role_name, ""),
                    "permissions": scopes,
                },
            )
            roles[role_name] = role
            action = "Created" if created else "Updated"
            self.stdout.write(f"  {action} role: {role_name} ({len(scopes)} resource scopes)")

        self.stdout.write("")

        # --- Upsert demo users ---
        for user_def in DEMO_USERS:
            role = roles[user_def["role_name"]]
            user, created = User.objects.update_or_create(
                username=user_def["username"],
                defaults={
                    "email": user_def["email"],
                    "first_name": user_def["first_name"],
                    "last_name": user_def["last_name"],
                    "is_staff": user_def["is_staff"],
                    "is_superuser": user_def["is_superuser"],
                    "role": role,
                },
            )
            user.set_password(DEFAULT_PASSWORD)
            user.save()
            action = "Created" if created else "Updated"
            self.stdout.write(f"  {action} user: {user_def['username']} (role={user_def['role_name']})")

            # Special handling for drivers: ensure they have a Driver profile
            if user_def["role_name"] == UserRole.DRIVER:
                driver_profile, created_p = Driver.objects.get_or_create(
                    user=user,
                    defaults={
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "driver_license_number": f"DL-{user.id:04d}",
                        "status": Driver.STATUS_ACTIVE,
                    },
                )
                if not created_p:
                    driver_profile.first_name = user.first_name
                    driver_profile.last_name = user.last_name
                    driver_profile.save()
                p_action = "Created" if created_p else "Linked"
                self.stdout.write(f"    {p_action} driver profile for {user.username}")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Done! All demo accounts use password: " + DEFAULT_PASSWORD))
        self.stdout.write("")
        self.stdout.write("  Demo accounts:")
        for u in DEMO_USERS:
            scopes = ROLE_SCOPES[u["role_name"]]
            scope_summary = ", ".join(
                f"{res}:{''.join(a[0].upper() for a in actions)}"
                for res, actions in scopes.items()
                if actions
            )
            self.stdout.write(f"    {u['username']:20s} [{u['role_name']:18s}] {scope_summary}")
