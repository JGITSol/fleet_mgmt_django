
import os
import sys
import django

# Setup Django environment
# Add the project root to sys.path
sys.path.append(r'D:\REPOS\fleet_mgmt_django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')
django.setup()

from CarFleetManagement.accounts.models import CustomUser

def reset_password():
    try:
        user = CustomUser.objects.get(username='testuser')
        user.set_password('password123')
        user.save()
        print(f"Successfully reset password for user: {user.username}")
    except CustomUser.DoesNotExist:
        print("User 'testuser' not found. Creating it...")
        CustomUser.objects.create_user('testuser', 'test@example.com', 'password123')
        print("Created user 'testuser'")

if __name__ == '__main__':
    reset_password()
