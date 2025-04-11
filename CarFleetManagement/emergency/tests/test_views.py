from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from emergency.models import EmergencyIncident, EmergencyResponse, EmergencyType, EmergencyStatus
from vehicles.models import Vehicle
from accounts.models import UserRole, Driver

User = get_user_model()

class EmergencyViewsTestCase(TestCase):
    """Test cases for the emergency app views."""
    
    def setUp(self):
        """Set up test environment."""
        # Create roles
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN, description='Administrator role')
        self.driver_role = UserRole.objects.create(name=UserRole.DRIVER, description='Driver role')
        
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=self.admin_role
        )
        
        self.driver_user = User.objects.create_user(
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
        
        # Create emergency incident
        self.incident = EmergencyIncident.objects.create(
            vehicle=self.vehicle,
            driver=self.driver,
            reported_by=self.driver_user,
            emergency_type=EmergencyType.BREAKDOWN,
            status=EmergencyStatus.REPORTED,
            location='Highway 101, Mile Marker 25',
            latitude=37.7749,
            longitude=-122.4194,
            description='Vehicle broke down with engine failure'
        )
        
        # Create emergency response
        self.response = EmergencyResponse.objects.create(
            incident=self.incident,
            responder=self.admin_user,
            action_taken='Dispatched tow truck to location',
            notes='ETA 30 minutes'
        )
        
        # Create client
        self.client = Client()
    
    def test_emergency_list_view(self):
        """Test emergency incident list view."""
        # Login as admin
        self.client.login(username='admin_user', password='password123')
        
        # Test emergency list view
        response = self.client.get(reverse('emergency_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Highway 101, Mile Marker 25')
        self.assertContains(response, 'BREAKDOWN')
    
    def test_emergency_detail_view(self):
        """Test emergency incident detail view."""
        # Login as admin
        self.client.login(username='admin_user', password='password123')
        
        # Test emergency detail view
        response = self.client.get(reverse('emergency_detail', kwargs={'pk': self.incident.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vehicle broke down with engine failure')
        self.assertContains(response, 'John Doe')
    
    def test_emergency_create_view(self):
        """Test emergency incident create view."""
        # Login as driver
        self.client.login(username='driver_user', password='password123')
        
        # Test GET request
        response = self.client.get(reverse('emergency_create'))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        incident_data = {
            'vehicle': self.vehicle.id,
            'driver': self.driver.id,
            'emergency_type': EmergencyType.ACCIDENT,
            'location': 'Intersection of Main St and 5th Ave',
            'latitude': 37.7833,
            'longitude': -122.4167,
            'description': 'Minor fender bender, no injuries'
        }
        
        response = self.client.post(reverse('emergency_create'), incident_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Verify incident was created
        self.assertTrue(EmergencyIncident.objects.filter(description='Minor fender bender, no injuries').exists())
    
    def test_emergency_update_view(self):
        """Test emergency incident update view."""
        # Login as admin
        self.client.login(username='admin_user', password='password123')
        
        # Test GET request
        response = self.client.get(reverse('emergency_update', kwargs={'pk': self.incident.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request - update status
        updated_data = {
            'vehicle': self.vehicle.id,
            'driver': self.driver.id,
            'emergency_type': EmergencyType.BREAKDOWN,
            'status': EmergencyStatus.RESPONDING,  # Changed from REPORTED to RESPONDING
            'location': 'Highway 101, Mile Marker 25',
            'latitude': 37.7749,
            'longitude': -122.4194,
            'description': 'Vehicle broke down with engine failure'
        }
        
        response = self.client.post(reverse('emergency_update', kwargs={'pk': self.incident.pk}), updated_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Verify incident was updated
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, EmergencyStatus.RESPONDING)
    
    def test_emergency_response_create_view(self):
        """Test emergency response create view."""
        # Login as admin
        self.client.login(username='admin_user', password='password123')
        
        # Test GET request
        response = self.client.get(reverse('emergency_response_create', kwargs={'incident_id': self.incident.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        response_data = {
            'incident': self.incident.id,
            'action_taken': 'Tow truck arrived at scene',
            'notes': 'Vehicle being towed to service center'
        }
        
        response = self.client.post(reverse('emergency_response_create', kwargs={'incident_id': self.incident.pk}), response_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Verify response was created
        self.assertTrue(EmergencyResponse.objects.filter(action_taken='Tow truck arrived at scene').exists())