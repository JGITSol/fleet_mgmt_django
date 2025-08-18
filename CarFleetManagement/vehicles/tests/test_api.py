from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken

# Model imports moved to setUp
from CarFleetManagement.vehicles.serializers import VehicleSerializer # Assuming serializer is safe for now
from tests.auth_test_mixin import AuthTestMixin
from tests.test_utils import authenticate_client
from tests.test_setup import setup_test_environment, get_authenticated_client

# Set up the test environment with all necessary patches
setup_test_environment()

class VehicleAPITestCase(APITestCase, AuthTestMixin):
    """Test cases for the Vehicle API endpoints."""
    
    def setUp(self):
        """Set up test environment."""
        from CarFleetManagement.vehicles.models import Vehicle
        from CarFleetManagement.accounts.models import UserRole, CustomUser
        self.Vehicle = Vehicle
        self.UserRole = UserRole
        self.CustomUser = CustomUser

        # Create roles
        self.admin_role = self.UserRole.objects.create(name=self.UserRole.ADMIN, description='Administrator role')
        self.driver_role = self.UserRole.objects.create(name=self.UserRole.DRIVER, description='Driver role')
        
        # Create users
        self.admin_user = self.CustomUser.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=self.admin_role
        )
        
        self.driver_user = self.CustomUser.objects.create_user(
            username='driver_user',
            email='driver@example.com',
            password='password123',
            role=self.driver_role
        )
        
        # Generate JWT tokens for potential use if specific tests need to switch users
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.driver_token = str(RefreshToken.for_user(self.driver_user).access_token)

        # Initialize client and authenticate as admin_user by default
        # self.client, _ = self.get_authenticated_client(self.admin_user) # Moved to individual tests
        
        # Create vehicles
        self.today = timezone.now().date()
        self.next_service = self.today + timedelta(days=90)
        self.insurance_expiry = self.today + timedelta(days=365)
        
        self.vehicle1 = self.Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2022,
            license_plate='ABC-123',
            vin='1HGCM82633A123456',
            color='Blue',
            fuel_type=self.Vehicle.FuelType.HYBRID,
            transmission=self.Vehicle.TransmissionType.AUTOMATIC,
            vehicle_type=self.Vehicle.VehicleType.SUV,
            mileage=15000,
            last_service_date=self.today - timedelta(days=90),
            next_service_date=self.next_service,
            insurance_expiry=self.insurance_expiry,
            status=self.Vehicle.Status.AVAILABLE
        )
        
        self.vehicle2 = self.Vehicle.objects.create(
            brand='Honda',
            model='Civic',
            year=2021,
            license_plate='XYZ-789',
            vin='2HGFG12633A654321',
            color='Red',
            fuel_type=self.Vehicle.FuelType.PETROL,
            transmission=self.Vehicle.TransmissionType.MANUAL,
            vehicle_type=self.Vehicle.VehicleType.TRUCK,
            mileage=25000,
            last_service_date=self.today - timedelta(days=30),
            next_service_date=self.today + timedelta(days=60),
            insurance_expiry=self.today + timedelta(days=300),
            status=self.Vehicle.Status.MAINTENANCE
        )
        
        # Assign vehicle to driver
        self.driver = self.driver_user
        if not hasattr(self.driver, 'assigned_vehicles'):
            from django.db import models
            self.driver.assigned_vehicles = models.Manager()
        # If Vehicle has a ManyToManyField to user, use that, else skip this assignment
        if hasattr(self.driver, 'assigned_vehicles') and hasattr(self.driver.assigned_vehicles, 'add'):
            self.driver.assigned_vehicles.add(self.vehicle1)
        
        # Create API client

        # client is already authenticated as admin_user from setUp
    
    def test_get_all_vehicles(self):
        """Test retrieving all vehicles."""
        self.client, _ = self.get_authenticated_client(self.admin_user)
        # client is already authenticated as admin_user from setUp
        # Make API request
        response = self.client.get(reverse('CarFleetManagement.api:api-vehicle-list'))
        
        # Get data from DB
        vehicles = self.Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_get_single_vehicle(self):
        """Test retrieving a single vehicle."""
        self.client, _ = self.get_authenticated_client(self.admin_user)
        # client is already authenticated as admin_user from setUp
        # Make API request
        response = self.client.get(reverse('CarFleetManagement.api:api-vehicle-detail', kwargs={'pk': self.vehicle1.pk}))
        
        # Get data from DB
        vehicle = self.Vehicle.objects.get(pk=self.vehicle1.pk)
        serializer = VehicleSerializer(vehicle)
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_vehicle(self):
        """Test creating a new vehicle."""
        self.client, _ = self.get_authenticated_client(self.admin_user)

        # Prepare data
        vehicle_data = {
            'brand': 'Ford',
            'model': 'F-150',
            'year': 2023,
            'license_plate': 'DEF-456',
            'vin': '3FTEW1EP5MFA12345',
            'color': 'Black',
            'fuel_type': self.Vehicle.FuelType.DIESEL,
            'transmission': self.Vehicle.TransmissionType.AUTOMATIC,
            'vehicle_type': self.Vehicle.VehicleType.PICKUP,
            'mileage': 5000,
            'status': self.Vehicle.Status.AVAILABLE
        }
        
        # client is already authenticated as admin_user from setUp
        # Make API request
        response = self.client.post(reverse('CarFleetManagement.api:api-vehicle-list'), vehicle_data, format='json')
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.Vehicle.objects.count(), 3)
        self.assertTrue(self.Vehicle.objects.filter(license_plate='DEF-456').exists())
    
    def test_update_vehicle(self):
        """Test updating a vehicle."""
        self.client, _ = self.get_authenticated_client(self.admin_user)

        # Prepare data
        updated_data = {
            'brand': 'Toyota',
            'model': 'Camry',
            'year': 2022,
            'license_plate': 'ABC-123',
            'vin': '1HGCM82633A123456',
            'color': 'Green',  # Changed from Blue to Green
            'fuel_type': self.Vehicle.FuelType.HYBRID,
            'transmission': self.Vehicle.TransmissionType.AUTOMATIC,
            'vehicle_type': self.Vehicle.VehicleType.SUV,
            'mileage': 16000,  # Updated mileage
            'status': self.Vehicle.Status.AVAILABLE
        }
        
        # client is already authenticated as admin_user from setUp
        # Make API request
        response = self.client.put(
            reverse('CarFleetManagement.api:api-vehicle-detail', kwargs={'pk': self.vehicle1.pk}),
            updated_data,
            format='json'
        )
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify vehicle was updated
        self.vehicle1.refresh_from_db()
        self.assertEqual(self.vehicle1.color, 'Green')
        self.assertEqual(self.vehicle1.mileage, 16000)
    
    def test_delete_vehicle(self):
        """Test deleting a vehicle."""
        self.client, _ = self.get_authenticated_client(self.admin_user)

        # client is already authenticated as admin_user from setUp
        # Make API request
        response = self.client.delete(reverse('CarFleetManagement.api:api-vehicle-detail', kwargs={'pk': self.vehicle2.pk}))
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertFalse(Vehicle.objects.filter(pk=self.vehicle2.pk).exists())
    
    def test_unauthorized_access(self):
        """Test unauthorized access to vehicle endpoints."""
        unauthenticated_client = APIClient()  # Create a new unauthenticated client for this specific test
        url = reverse('CarFleetManagement.api:api-vehicle-list')
        response = unauthenticated_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Authenticate as driver (who may have limited permissions)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.driver_token}')
        
        # Try to delete a vehicle (assuming drivers can't delete vehicles)
        response = self.client.delete(reverse('CarFleetManagement.api:api-vehicle-detail', kwargs={'pk': self.vehicle2.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)