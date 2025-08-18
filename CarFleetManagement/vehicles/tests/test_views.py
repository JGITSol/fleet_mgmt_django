from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from CarFleetManagement.vehicles.models import Vehicle
from CarFleetManagement.accounts.models import UserRole

User = get_user_model()

# ========================
# Appended from project-level tests/test_vehicles.py
# ========================
import pytest
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta

from CarFleetManagement.vehicles.models import Vehicle

# Import tests from the app-specific test directory
from .test_models import VehicleTestCase

# Add additional tests that might require fixtures from conftest.py
@pytest.mark.django_db
def test_vehicle_status_update(vehicle):
    """Test updating vehicle status."""
    # Test changing status
    vehicle.status = Vehicle.Status.MAINTENANCE
    vehicle.save()
    
    # Retrieve from DB and verify
    updated_vehicle = Vehicle.objects.get(id=vehicle.id)
    assert updated_vehicle.status == Vehicle.Status.MAINTENANCE

@pytest.mark.django_db
def test_vehicle_mileage_update(vehicle):
    """Test updating vehicle mileage."""
    # Update mileage
    new_mileage = vehicle.mileage + 1000
    vehicle.mileage = new_mileage
    vehicle.save()
    
    # Retrieve from DB and verify
    updated_vehicle = Vehicle.objects.get(id=vehicle.id)
    assert updated_vehicle.mileage == new_mileage

@pytest.mark.django_db
def test_vehicle_service_due(vehicle):
    """Test service due calculation."""
    # Set next service date to yesterday
    yesterday = timezone.now().date() - timedelta(days=1)
    vehicle.next_service_date = yesterday
    vehicle.save()
    
    # Retrieve from DB and verify
    updated_vehicle = Vehicle.objects.get(id=vehicle.id)
    assert updated_vehicle.is_service_due()

from rest_framework_simplejwt.tokens import RefreshToken

class VehicleViewsTestCase(APITestCase):
    """Test cases for the vehicles app views."""
    
    def setUp(self):
        """Set up test environment."""
        # Create roles
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN, description='Administrator role')
        self.fleet_manager_role = UserRole.objects.create(name=UserRole.MANAGER, description='Fleet Manager role')
        
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=self.admin_role
        )
        
        self.fleet_manager_user = User.objects.create_user(
            username='fleet_manager',
            email='fleet@example.com',
            password='password123',
            role=self.fleet_manager_role
        )
        
        # Create vehicles
        self.today = timezone.now().date()
        self.next_service = self.today + timedelta(days=90)
        self.insurance_expiry = self.today + timedelta(days=365)
        
        self.vehicle1 = Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2022,
            license_plate='ABC-123',
            vin='1HGCM82633A123456',
            color='Blue',
            fuel_type=Vehicle.FuelType.HYBRID,
            transmission=Vehicle.TransmissionType.AUTOMATIC,
            vehicle_type=Vehicle.VehicleType.SUV,
            mileage=15000,
            last_service_date=self.today - timedelta(days=90),
            next_service_date=self.next_service,
            insurance_expiry=self.insurance_expiry,
            status=Vehicle.Status.AVAILABLE
        )
        
        self.vehicle2 = Vehicle.objects.create(
            brand='Honda',
            model='Civic',
            year=2021,
            license_plate='XYZ-789',
            vin='2HGFG12633A654321',
            color='Red',
            fuel_type=Vehicle.FuelType.PETROL,
            transmission=Vehicle.TransmissionType.MANUAL,
            vehicle_type=Vehicle.VehicleType.TRUCK,
            mileage=25000,
            last_service_date=self.today - timedelta(days=30),
            next_service_date=self.today + timedelta(days=60),
            insurance_expiry=self.today + timedelta(days=300),
            status=Vehicle.Status.MAINTENANCE
        )
        
        # Create client

        
    def authenticate_as(self, user):
        """Authenticate as a user using JWT."""
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def test_vehicle_list_view(self):
        """Test vehicle list view."""
        self.authenticate_as(self.admin_user)
        response = self.client.get(reverse('vehicles:vehicle_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Toyota Camry')
        self.assertContains(response, 'Honda Civic')
    
    def test_vehicle_detail_view(self):
        """Test vehicle detail view."""
        self.authenticate_as(self.admin_user)
        response = self.client.get(reverse('vehicles:vehicle_detail', kwargs={'pk': self.vehicle1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Toyota Camry')
        self.assertContains(response, 'ABC-123')
    
    def test_vehicle_create_view(self):
        """Test vehicle create view."""
        self.authenticate_as(self.fleet_manager_user)
        response = self.client.get(reverse('vehicles:vehicle_create'))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        vehicle_data = {
            'brand': 'Ford',
            'model': 'F-150',
            'year': 2023,
            'license_plate': 'DEF-456',
            'vin': '3FTEW1EP5MFA12345',
            'color': 'Black',
            'fuel_type': Vehicle.FuelType.DIESEL,
            'transmission': Vehicle.TransmissionType.AUTOMATIC,
            'vehicle_type': Vehicle.VehicleType.PICKUP,
            'mileage': 5000,
            'status': Vehicle.Status.AVAILABLE
        }
        
        response = self.client.post(reverse('vehicles:vehicle_create'), vehicle_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Verify vehicle was created
        self.assertTrue(Vehicle.objects.filter(license_plate='DEF-456').exists())
    
    def test_vehicle_update_view(self):
        """Test vehicle update view."""
        self.authenticate_as(self.fleet_manager_user)
        response = self.client.get(reverse('vehicles:vehicle_update', kwargs={'pk': self.vehicle1.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        updated_data = {
            'brand': 'Toyota',
            'model': 'Camry',
            'year': 2022,
            'license_plate': 'ABC-123',
            'vin': '1HGCM82633A123456',
            'color': 'Green',  # Changed from Blue to Green
            'fuel_type': Vehicle.FuelType.HYBRID,
            'transmission': Vehicle.TransmissionType.AUTOMATIC,
            'vehicle_type': Vehicle.VehicleType.SUV,
            'mileage': 16000,
            'status': Vehicle.Status.AVAILABLE
        }
        
        response = self.client.post(reverse('vehicles:vehicle_update', kwargs={'pk': self.vehicle1.pk}), updated_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Verify vehicle was updated
        self.vehicle1.refresh_from_db()
        self.assertEqual(self.vehicle1.color, 'Green')
        self.assertEqual(self.vehicle1.mileage, 16000)
        
    def test_vehicle_delete_view(self):
        """Test vehicle delete view."""
        self.authenticate_as(self.fleet_manager_user)
        response = self.client.delete(reverse('vehicles:vehicle_delete', kwargs={'pk': self.vehicle2.pk}))
        self.assertEqual(response.status_code, 302) # Redirect after successful deletion
        
        # Verify vehicle was deleted
        self.assertFalse(Vehicle.objects.filter(pk=self.vehicle2.pk).exists())