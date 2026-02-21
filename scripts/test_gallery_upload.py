import os
import sys
import django
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path

# Fix python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings.dev')
django.setup()

from CarFleetManagement.accounts.models import CustomUser
from CarFleetManagement.vehicles.models import Vehicle, VehicleMedia

from rest_framework_simplejwt.tokens import RefreshToken

def test_gallery_internal():
    client = Client()
    
    # 1. Get or create a user
    user = CustomUser.objects.filter(is_superuser=True).first()
    if not user:
        user = CustomUser.objects.create_superuser('admin_test', 'admin@test.com', 'password123')
    
    print(f"Using user: {user.username}")
    
    # Generate JWT Token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    auth_header = f"Bearer {access_token}"

    # 2. Get a vehicle
    vehicle = Vehicle.objects.first()
    if not vehicle:
        vehicle = Vehicle.objects.create(license_plate="TEST-X1", brand="Test", model="Model X")
    
    print(f"Using vehicle: {vehicle.license_plate} (ID: {vehicle.id})")

    # 3. Create a dummy file
    file_content = b"fake image content"
    test_file = SimpleUploadedFile("test_gallery.png", file_content, content_type="image/png")

    # 4. Post to API
    from django.urls import reverse
    url = reverse('api:api-vehicle-media-list')
    print(f"URL: {url}")
    data = {
        "vehicle": vehicle.id,
        "media_type": "IMAGE",
        "title": "Internal Test Image",
        "description": "Uploaded via internal script",
        "file": test_file
    }
    
    print(f"Posting to {url}...")
    response = client.post(
        url, 
        data, 
        HTTP_ACCEPT='application/json',
        HTTP_AUTHORIZATION=auth_header
    )
    
    print(f"Status Code: {response.status_code}")
    if hasattr(response, 'data'):
        print(f"Data: {response.data}")
    else:
        print(f"Content: {response.content[:1000]}")

    if response.status_code == 201:
        print("Success! Created VehicleMedia entry.")
        # Verify it exists in DB
        media_count = VehicleMedia.objects.filter(vehicle=vehicle).count()
        print(f"Total media items in DB for this vehicle: {media_count}")

        # Test GET
        print(f"Testing GET {url}?vehicle={vehicle.id}...")
        response = client.get(
            f"{url}?vehicle={vehicle.id}",
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION=auth_header
        )
        print(f"GET Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Received {len(response.data)} items.")
            print(f"First item: {response.data[0]}")
    else:
        print(f"Failed with status {response.status_code}")

if __name__ == "__main__":
    test_gallery_internal()
