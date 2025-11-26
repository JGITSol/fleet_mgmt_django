import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    user = User.objects.get(username='admin')
    print(f"User exists: {user.username}")
    
    # Force set password
    print("Force setting password to 'TestPassword123!'...")
    user.set_password("TestPassword123!")
    user.save()
    
    # Verify again
    user.refresh_from_db()
    is_valid = user.check_password("TestPassword123!")
    print(f"Password valid after reset: {is_valid}")
    
except User.DoesNotExist:
    print("User 'admin' does not exist")
except Exception as e:
    print(f"Error: {e}")
