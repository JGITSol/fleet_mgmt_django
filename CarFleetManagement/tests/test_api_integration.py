import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestAPIIntegration:
    @pytest.fixture(autouse=True)
    def setup_client(self):
        self.client = APIClient()

    def test_auth_and_profile_flow(self, user):
        """Test login and then fetching profile with JWT."""
        # Reset password to known one for test
        user.set_password("TestPassword123!")
        user.save()

        # Login
        url = reverse('api:auth_login')
        response = self.client.post(url, {
            "username": user.username,
            "password": "TestPassword123!"
        })
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Fetch Profile
        url = reverse('api:auth_profile')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username

    def test_vehicle_list_unauthenticated(self):
        """Test that vehicle list requires authentication."""
        url = reverse('api:vehicle-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_vehicle_crud_as_admin(self, custom_user):
        """Test full vehicle CRUD as a user with admin role."""
        from CarFleetManagement.accounts.models import UserRole
        admin_role, _ = UserRole.objects.get_or_create(name=UserRole.ADMIN)
        custom_user.role = admin_role
        custom_user.save()

        # Auth
        refresh = RefreshToken.for_user(custom_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Create Vehicle
        url = reverse('api:vehicle-list')
        data = {
            "brand": "Tesla",
            "model": "Model 3",
            "year": 2023,
            "license_plate": "TEST-123",
            "vin": "TESTVIN1234567890",
            "mileage": 0,
            "status": "AVAILABLE"
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        vehicle_id = response.data['id']

        # Update Vehicle
        url = reverse('CarFleetManagement.api:vehicle-detail', args=[vehicle_id])
        response = self.client.patch(url, {"mileage": 100})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['mileage'] == 100

        # Delete Vehicle
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

from rest_framework_simplejwt.tokens import RefreshToken
