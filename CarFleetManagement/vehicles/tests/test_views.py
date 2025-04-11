from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from vehicles.models import Vehicle
from accounts.models import UserRole, Driver

User = get_user_model()

class VehicleViewsTestCase(TestCase):
    """Test cases for the vehicles app views."""
    
    def setUp(self):
        """Set up test environment."""
        # Create roles
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN, description='Administrator role')
        self.fleet_manager_role = UserRole.objects.create(name=UserRole.FLEET_MANAGER, description='Fleet Manager role')
        
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
        self.client = Client()
    
    def test_vehicle_list_view(self):
        """Test vehicle list view."""
        # Login as admin
        self.client.login(username='admin_user', password='password123')
        
        # Test vehicle list view
        response = self.client.get(reverse('vehicle_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Toyota Camry')
        self.assertContains(response, 'Honda Civic')
    
    def test_vehicle_detail_view(self):
        """Test vehicle detail view."""
        # Login as admin
        self.client.login(username='admin_user', password='password123')
        
        # Test vehicle detail view
        response = self.client.get(reverse('vehicle_detail', kwargs={'pk': self.vehicle1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Toyota Camry')
        self.assertContains(response, 'ABC-123')
    
    def test_vehicle_create_view(self):
        """Test vehicle create view."""
        # Login as fleet manager
        self.client.login(username='fleet_manager', password='password123')
        
        # Test GET request
        response = self.client.get(reverse('vehicle_create'))
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
        
        response = self.client.post(reverse('vehicle_create'), vehicle_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Verify vehicle was created
        self.assertTrue(Vehicle.objects.filter(license_plate='DEF-456').exists())
    
    def test_vehicle_update_view(self):
        """Test vehicle update view."""
        # Login as fleet manager
        self.client.login(username='fleet_manager', password='password123')
        
        # Test GET request
        response = self.client.get(reverse('vehicle_update', kwargs={'pk': self.vehicle1.pk}))
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
            'mileage': 16000,  # Updated mileage
            'status': Vehicle.Status.AVAILABLE
        }
        
        response = self.client.post(reverse('vehicle_update', kwargs={'pk': self.vehicle1.pk}), updated_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Verify vehicle was updated
        self.vehicle1.refresh_from_db()
        self.assertEqual(self.vehicle1.color, 'Green')
        self.assertEqual(self.vehicle1.mileage, 16000)