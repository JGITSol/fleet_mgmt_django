from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from accounts.models import Driver, UserRole, CustomUser
from accounts.serializers import DriverSerializer
from vehicles.models import Vehicle

class DriverAPITestCase(TestCase):
    """Test cases for the Driver API endpoints."""
    
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
        
        # Create vehicle
        self.vehicle = Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2022,
            license_plate='ABC-123',
            vin='1HGCM82633A123456'
        )
        
        # Create drivers
        self.driver1 = Driver.objects.create(
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
        
        self.driver2 = Driver.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone_number='987-654-3210',
            driver_license_number='DL87654321',
            license_expiry_date=timezone.now().date() + timedelta(days=180),
            status='ACTIVE',
            hire_date=timezone.now().date() - timedelta(days=90)
        )
        
        # Assign vehicle to driver
        self.driver1.assigned_vehicles.add(self.vehicle)
        
        # Create API client
        self.client = APIClient()
    
    def test_get_all_drivers(self):
        """Test retrieving all drivers."""
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Make API request
        response = self.client.get(reverse('api-driver-list'))
        
        # Get data from DB
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_get_single_driver(self):
        """Test retrieving a single driver."""
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Make API request
        response = self.client.get(reverse('api-driver-detail', kwargs={'pk': self.driver1.pk}))
        
        # Get data from DB
        driver = Driver.objects.get(pk=self.driver1.pk)
        serializer = DriverSerializer(driver)
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_driver(self):
        """Test creating a new driver."""
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Prepare data
        driver_data = {
            'first_name': 'Robert',
            'last_name': 'Johnson',
            'email': 'robert.johnson@example.com',
            'phone_number': '555-123-4567',
            'driver_license_number': 'DL55512345',
            'license_expiry_date': (timezone.now().date() + timedelta(days=730)).isoformat(),
            'status': 'ACTIVE',
            'hire_date': timezone.now().date().isoformat()
        }
        
        # Make API request
        response = self.client.post(reverse('api-driver-list'), driver_data, format='json')
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 3)
        self.assertTrue(Driver.objects.filter(email='robert.johnson@example.com').exists())
    
    def test_update_driver(self):
        """Test updating a driver."""
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Prepare data
        updated_data = {
            'first_name': 'Jane',
            'last_name': 'Smith-Johnson',  # Changed last name
            'email': 'jane.smith@example.com',
            'phone_number': '987-654-3210',
            'driver_license_number': 'DL87654321',
            'license_expiry_date': (timezone.now().date() + timedelta(days=180)).isoformat(),
            'status': 'ACTIVE',
            'hire_date': (timezone.now().date() - timedelta(days=90)).isoformat()
        }
        
        # Make API request
        response = self.client.put(
            reverse('api-driver-detail', kwargs={'pk': self.driver2.pk}),
            updated_data,
            format='json'
        )
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify driver was updated
        self.driver2.refresh_from_db()
        self.assertEqual(self.driver2.last_name, 'Smith-Johnson')
    
    def test_delete_driver(self):
        """Test deleting a driver."""
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Make API request
        response = self.client.delete(reverse('api-driver-detail', kwargs={'pk': self.driver2.pk}))
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Driver.objects.count(), 1)
        self.assertFalse(Driver.objects.filter(pk=self.driver2.pk).exists())
    
    def test_unauthorized_access(self):
        """Test unauthorized access to driver API."""
        # Unauthenticated request
        response = self.client.get(reverse('api-driver-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Create a regular user without admin permissions
        regular_user = CustomUser.objects.create_user(
            username='regular_user',
            email='regular@example.com',
            password='password123'
        )
        
        # Authenticate as regular user
        self.client.force_authenticate(user=regular_user)
        
        # Try to delete a driver
        response = self.client.delete(reverse('api-driver-detail', kwargs={'pk': self.driver2.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)