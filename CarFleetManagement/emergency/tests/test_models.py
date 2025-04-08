from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal

from emergency.models import EmergencyIncident, EmergencyResponse, EmergencyType, EmergencyStatus, EmergencyContact
from vehicles.models import Vehicle
from accounts.models import UserRole, Driver

User = get_user_model()

class EmergencyIncidentTestCase(TestCase):
    """Test cases for the EmergencyIncident model."""
    
    def setUp(self):
        """Set up test environment."""
        # Create roles
        self.driver_role = UserRole.objects.create(name=UserRole.DRIVER)
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN)
        
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
            license_expiry_date=timezone.now().date() + timezone.timedelta(days=365),
            hire_date=timezone.now().date() - timezone.timedelta(days=30)
        )
        
        # Create emergency incident
        self.incident = EmergencyIncident.objects.create(
            vehicle=self.vehicle,
            driver=self.driver,
            reported_by=self.admin_user,
            emergency_type=EmergencyType.ACCIDENT,
            status=EmergencyStatus.REPORTED,
            location='Highway 101, Mile Marker 25',
            latitude=Decimal('37.7749'),
            longitude=Decimal('-122.4194'),
            description='Vehicle involved in a minor collision.'
        )
    
    def test_incident_creation(self):
        """Test EmergencyIncident creation."""
        self.assertEqual(self.incident.vehicle, self.vehicle)
        self.assertEqual(self.incident.driver, self.driver)
        self.assertEqual(self.incident.reported_by, self.admin_user)
        self.assertEqual(self.incident.emergency_type, EmergencyType.ACCIDENT)
        self.assertEqual(self.incident.status, EmergencyStatus.REPORTED)
        self.assertEqual(self.incident.location, 'Highway 101, Mile Marker 25')
        self.assertEqual(self.incident.latitude, Decimal('37.7749'))
        self.assertEqual(self.incident.longitude, Decimal('-122.4194'))
        self.assertEqual(self.incident.description, 'Vehicle involved in a minor collision.')
        self.assertIsNotNone(self.incident.reported_time)
        self.assertIsNone(self.incident.resolved_time)
    
    def test_incident_string_representation(self):
        """Test EmergencyIncident string representation."""
        expected_str = f"Accident - Toyota Camry (ABC-123) - {self.incident.reported_time.strftime('%Y-%m-%d %H:%M')}"
        self.assertEqual(str(self.incident), expected_str)
    
    def test_incident_status_update(self):
        """Test updating EmergencyIncident status."""
        # Update to responding
        self.incident.status = EmergencyStatus.RESPONDING
        self.incident.save()
        self.assertEqual(self.incident.status, EmergencyStatus.RESPONDING)
        
        # Update to resolved
        self.incident.status = EmergencyStatus.RESOLVED
        self.incident.resolved_time = timezone.now()
        self.incident.save()
        self.assertEqual(self.incident.status, EmergencyStatus.RESOLVED)
        self.assertIsNotNone(self.incident.resolved_time)
        
        # Update to closed
        self.incident.status = EmergencyStatus.CLOSED
        self.incident.save()
        self.assertEqual(self.incident.status, EmergencyStatus.CLOSED)

class EmergencyResponseTestCase(TestCase):
    """Test cases for the EmergencyResponse model."""
    
    def setUp(self):
        """Set up test environment."""
        # Create roles
        self.driver_role = UserRole.objects.create(name=UserRole.DRIVER)
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN)
        
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=self.admin_role
        )
        
        self.responder_user = User.objects.create_user(
            username='responder_user',
            email='responder@example.com',
            password='password123',
            role=self.admin_role
        )
        
        # Create vehicle
        self.vehicle = Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2022,
            license_plate='ABC-123',
            vin='1HGCM82633A123456'
        )
        
        # Create emergency incident
        self.incident = EmergencyIncident.objects.create(
            vehicle=self.vehicle,
            reported_by=self.admin_user,
            emergency_type=EmergencyType.BREAKDOWN,
            status=EmergencyStatus.REPORTED,
            location='Highway 101, Mile Marker 25',
            description='Vehicle engine failure.'
        )
        
        # Create emergency response
        self.response = EmergencyResponse.objects.create(
            incident=self.incident,
            responder=self.responder_user,
            action_taken='Dispatched tow truck to location.',
            notes='ETA 30 minutes.'
        )
    
    def test_response_creation(self):
        """Test EmergencyResponse creation."""
        self.assertEqual(self.response.incident, self.incident)
        self.assertEqual(self.response.responder, self.responder_user)
        self.assertEqual(self.response.action_taken, 'Dispatched tow truck to location.')
        self.assertEqual(self.response.notes, 'ETA 30 minutes.')
        self.assertIsNotNone(self.response.response_time)
    
    def test_response_string_representation(self):
        """Test EmergencyResponse string representation."""
        expected_str = f"Response to {self.incident} by {self.responder_user.username}"
        self.assertEqual(str(self.response), expected_str)

class EmergencyContactTestCase(TestCase):
    """Test cases for the EmergencyContact model in the emergency app."""
    
    def setUp(self):
        """Set up test environment."""
        self.user = User.objects.create_user(
            username='test_user',
            email='user@example.com',
            password='password123'
        )
        
        self.emergency_contact = EmergencyContact.objects.create(
            user=self.user,
            name='Jane Doe',
            phone_number='123-456-7890',
            relationship='Spouse'
        )
    
    def test_emergency_contact_creation(self):
        """Test EmergencyContact creation."""
        self.assertEqual(self.emergency_contact.name, 'Jane Doe')
        self.assertEqual(self.emergency_contact.phone_number, '123-456-7890')
        self.assertEqual(self.emergency_contact.relationship, 'Spouse')
        self.assertEqual(self.emergency_contact.user, self.user)
    
    def test_emergency_contact_string_representation(self):
        """Test EmergencyContact string representation."""
        expected_str = f"Jane Doe (Spouse of {self.user.username})"
        self.assertEqual(str(self.emergency_contact), expected_str)