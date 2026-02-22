import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings.dev')

import django
django.setup()

from CarFleetManagement.accounts.models import CustomUser, UserRole

print("=== ROLES ===")
for r in UserRole.objects.all():
    print(f"  ROLE id={r.id}")
    print(f"       name={r.name}")
    print(f"       desc={r.description}")
    print(f"       perms={r.permissions}")
    print()

print()
print("=== USERS ===")
for u in CustomUser.objects.all():
    print(f"  USER id={u.id}")
    print(f"       username={u.username}")
    print(f"       email={u.email}")
    print(f"       staff={u.is_staff}")
    print(f"       super={u.is_superuser}")
    print(f"       role_id={u.role_id}")
    print()
