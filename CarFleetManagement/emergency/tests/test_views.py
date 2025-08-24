from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

# Model imports moved into setUp methods or test functions
from .jwt_test_mixin import JWTAuthTestMixin

User = get_user_model()

# ========================
# Appended from project-level tests/test_emergency.py
# ========================
import pytest
from django.utils import timezone
from datetime import timedelta

# Model imports moved into test functions or handled by fixtures

# Add additional tests that might require fixtures from conftest.py
@pytest.mark.django_db
def test_emergency_contact_creation(emergency_contact, custom_user):
    """Test emergency contact creation using fixture."""
    from CarFleetManagement.emergency.models import EmergencyContact
    # Retrieve from DB and verify
    contact = EmergencyContact.objects.get(user=custom_user)
    assert contact.name == 'Jane Doe'
    assert contact.relationship == 'Spouse'
    assert contact.phone_number == '1234567890'

@pytest.mark.django_db
def test_emergency_incident_creation(emergency_incident, vehicle, custom_user):
    """Test emergency incident creation using fixture."""
    from CarFleetManagement.emergency.models import EmergencyIncident
    # Retrieve from DB and verify
    incident = EmergencyIncident.objects.get(vehicle=vehicle)
    assert incident.emergency_type == 'ACCIDENT'
    assert incident.status == 'REPORTED'
    assert incident.reported_by == custom_user
    assert incident.location == 'Test Location'

@pytest.mark.django_db
def test_emergency_contact_str_representation(emergency_contact):
    """Test string representation of EmergencyContact."""
    # The string representation depends on the __str__ method implementation
    # This is a basic check that the string representation is not empty
    assert str(emergency_contact) != ''

@pytest.mark.django_db
def test_emergency_incident_status_update(emergency_incident):
    """Test emergency incident status update."""
    # Mark as resolved
    emergency_incident.status = 'RESOLVED'
    emergency_incident.resolved_time = timezone.now()
    emergency_incident.save()
    
    # Verify it's now resolved
    from CarFleetManagement.emergency.models import EmergencyIncident # Import for this specific call
    updated_incident = EmergencyIncident.objects.get(id=emergency_incident.id)
    assert updated_incident.status == 'RESOLVED'
    assert updated_incident.resolved_time is not None

from rest_framework_simplejwt.tokens import RefreshToken

class EmergencyViewsTestCase(JWTAuthTestMixin, APITestCase):
    """Test cases for the emergency app views."""
    
    def setUp(self):
        """Set up test environment."""
        from CarFleetManagement.accounts.models import UserRole, Driver
        from CarFleetManagement.vehicles.models import Vehicle
        from CarFleetManagement.emergency.models import EmergencyIncident, EmergencyType, EmergencyStatus, EmergencyResponse

        self.UserRole = UserRole
        self.Driver = Driver
        self.Vehicle = Vehicle
        self.EmergencyIncident = EmergencyIncident
        self.EmergencyType = EmergencyType
        self.EmergencyStatus = EmergencyStatus
        self.EmergencyResponse = EmergencyResponse

        # Create roles
        self.admin_role = self.UserRole.objects.create(name=self.UserRole.ADMIN, description='Administrator role')
        self.driver_role = self.UserRole.objects.create(name=self.UserRole.DRIVER, description='Driver role')
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
        # Authenticate as admin by default for admin-required tests
        self.authenticate_client(user=self.admin_user)

        # Create vehicle
        self.vehicle = self.Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2022,
            license_plate='ABC-123',
            vin='1HGCM82633A123456'
        )
        # Create driver
        self.driver = self.Driver.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='123-456-7890',
            driver_license_number='DL12345678'
        )
        
        # Create emergency incident
        self.incident = self.EmergencyIncident.objects.create(
            vehicle=self.vehicle,
            driver=self.driver,
            reported_by=self.admin_user,  # Always use authenticated user for reported_by
            emergency_type=self.EmergencyType.BREAKDOWN,
            status=self.EmergencyStatus.REPORTED,
            location='Highway 101, Mile Marker 25',
            latitude=37.7749,
            longitude=-122.4194,
            description='Vehicle broke down with engine failure'
        )
        
        # Create emergency response
        self.response = self.EmergencyResponse.objects.create(
            incident=self.incident,
            responder=self.admin_user,
            action_taken='Dispatched tow truck to location.',
            notes='ETA 30 minutes.'
        )
        

    
    def test_emergency_list_view(self):
        """Test emergency incident list view."""
        # Login as admin
        self.authenticate_client(user=self.admin_user)
        
        # Test emergency list view
        response = self.client.get(reverse('CarFleetManagement.api:api-emergency-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Highway 101, Mile Marker 25')
        self.assertContains(response, 'BREAKDOWN')
    
    def test_emergency_detail_view(self):
        """Test emergency incident detail view."""
        # Login as admin
        self.authenticate_client(user=self.admin_user)
        
        # Test emergency detail view
        response = self.client.get(reverse('CarFleetManagement.api:api-emergency-detail', kwargs={'pk': self.incident.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vehicle broke down with engine failure')
        self.assertContains(response, 'John Doe')
    
    def test_emergency_create_view(self):
        """Test emergency incident create view."""  
        # Login as driver
        self.authenticate_client(user=self.driver_user)

        # Test GET request
        response = self.client.get(reverse('CarFleetManagement.api:api-emergency-list'))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        # Do not include 'reported_by' in form data; view sets it automatically
        incident_data = {
            'vehicle': self.vehicle.id,
            'emergency_type': self.EmergencyType.ACCIDENT,
            'location': 'Elm Street, Near Main Ave',
            'status': self.EmergencyStatus.REPORTED,
            'description': 'Minor fender bender, no injuries'
        }
        
        response = self.client.post(reverse('CarFleetManagement.api:api-emergency-list'), incident_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Verify incident was created
        self.assertTrue(self.EmergencyIncident.objects.filter(description='Minor fender bender, no injuries').exists())
    
    def test_emergency_update_view(self):
        """Test emergency incident update view."""
        # Login as admin
        self.authenticate_client(user=self.admin_user)

        # Test GET request
        response = self.client.get(
            reverse('CarFleetManagement.api:api-emergency-detail', kwargs={'pk': self.incident.pk})
        )
        self.assertEqual(response.status_code, 200)

        # Test POST request - update status
        updated_data = {
            'vehicle': self.vehicle.id,
            'driver': self.driver.id,
            'emergency_type': self.EmergencyType.BREAKDOWN,
            'status': self.EmergencyStatus.RESPONDING,  # Changed from REPORTED to RESPONDING
            'location': 'Highway 101, Mile Marker 25',
            'latitude': 37.7749,
            'longitude': -122.4194,
            'description': 'Vehicle broke down with engine failure'
        }

        response = self.client.post(
            reverse('CarFleetManagement.api:api-emergency-detail', kwargs={'pk': self.incident.pk}),
            updated_data,
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update

        # Verify incident was updated
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, self.EmergencyStatus.RESPONDING)

    
    def test_emergency_response_create_view(self):
        """Test emergency response create view."""
        # Login as admin
        self.authenticate_client(user=self.admin_user)
        
        # Test GET request
        response = self.client.get(reverse('CarFleetManagement.api:api-emergency-response-list')) # GET not typical for create, but reflects old test
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        response_data = {
            'action_taken': 'Towed vehicle to service center',
            'notes': 'Vehicle being towed to service center'
        }

        response_data['incident'] = self.incident.pk  # Add incident_id to POST data
        response = self.client.post(reverse('CarFleetManagement.api:api-emergency-response-list'), response_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation

        # Verify response was created
        self.assertTrue(self.EmergencyResponse.objects.filter(notes='Vehicle being towed to service center').exists())

