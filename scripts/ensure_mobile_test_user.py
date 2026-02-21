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
USERNAME = 'mobiletestuser'
PASSWORD = 'mobiletestpassword1337'
EMAIL = 'mobiletestuser@example.com'

try:
    user, created = User.objects.get_or_create(username=USERNAME, defaults={'email': EMAIL})
    
    if created:
        print(f"User '{USERNAME}' created.")
        user.set_password(PASSWORD)
        user.save()
        print(f"Password set for '{USERNAME}'.")
    else:
        print(f"User '{USERNAME}' already exists.")
        # Ensure password is correct
        if not user.check_password(PASSWORD):
            print(f"Password for '{USERNAME}' was incorrect. Resetting to '{PASSWORD}'...")
            user.set_password(PASSWORD)
            user.save()
            print(f"Password reset for '{USERNAME}'.")
        else:
            print(f"Password for '{USERNAME}' is correct.")

except Exception as e:
    print(f"Error: {e}")
