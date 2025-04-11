from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from vehicles.models import Vehicle
from vehicles.serializers import VehicleSerializer
from accounts.models import UserRole, Driver, CustomUser

class VehicleAPITestCase(TestCase):
    """Test cases for the Vehicle API endpoints."""
    
    def setUp(self):
        """Set up test environment."""
        # Create roles
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN, description='Administrator role')
        self.driver_role = UserRole.objects.create(name=UserRole.DRIVER, description='Driver role')
        
        # Create users
        self.admin_user = CustomUser.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=self.admin_role
        )
        
        self.driver_user = CustomUser.objects.create_user(
            username='driver_user',
            email='driver@example.com',
            password='password123',
            role=self.driver_role
        )
        
        # Create driver
        self.driver = Driver.objects.create(
            user=self.driver_user,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='123-456-7890',
            driver_license_number='DL12345678',
            license_expiry_date=timezone.now().date() + timedelta(days=365),
            status='ACTIVE',
            hire_date=timezone.now().date() - timedelta(days=180)
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
        
        # Assign vehicle to driver
        self.driver.assigned_vehicles.add(self.vehicle1)
        
        # Create API client
        self.client = APIClient()
    
    def test_get_all_vehicles(self):
        """Test retrieving all vehicles."""
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Make API request
        response = self.client.get(reverse('api-vehicle-list'))
        
        # Get data from DB
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_get_single_vehicle(self):
        """Test retrieving a single vehicle."""
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Make API request
        response = self.client.get(reverse('api-vehicle-detail', kwargs={'pk': self.vehicle1.pk}))
        
        # Get data from DB
        vehicle = Vehicle.objects.get(pk=self.vehicle1.pk)
        serializer = VehicleSerializer(vehicle)
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_vehicle(self):
        """Test creating a new vehicle."""
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Prepare data
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
        
        # Make API request
        response = self.client.post(reverse('api-vehicle-list'), vehicle_data, format='json')
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 3)
        self.assertTrue(Vehicle.objects.filter(license_plate='DEF-456').exists())
    
    def test_update_vehicle(self):
        """Test updating a vehicle."""
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Prepare data
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
            'mileage': 16000,  # Updated mileage
            'status': Vehicle.Status.AVAILABLE
        }
        
        # Make API request
        response = self.client.put(
            reverse('api-vehicle-detail', kwargs={'pk': self.vehicle1.pk}),
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
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Make API request
        response = self.client.delete(reverse('api-vehicle-detail', kwargs={'pk': self.vehicle2.pk}))
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertFalse(Vehicle.objects.filter(pk=self.vehicle2.pk).exists())
    
    def test_unauthorized_access(self):
        """Test unauthorized access to vehicle API."""
        # Unauthenticated request
        response = self.client.get(reverse('api-vehicle-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Authenticate as driver (who may have limited permissions)
        self.client.force_authenticate(user=self.driver_user)
        
        # Try to delete a vehicle (assuming drivers can't delete vehicles)
        response = self.client.delete(reverse('api-vehicle-detail', kwargs={'pk': self.vehicle2.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)