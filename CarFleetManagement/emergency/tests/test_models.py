from decimal import Decimal

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

# Model imports moved into setUp methods

User = get_user_model()

class EmergencyIncidentTestCase(APITestCase):
    """Test cases for the EmergencyIncident model."""

    def setUp(self):
        """Set up test environment."""
        from CarFleetManagement.accounts.models import Driver, UserRole
        from CarFleetManagement.emergency.models import (
            EmergencyIncident,
            EmergencyStatus,
            EmergencyType,
        )
        from CarFleetManagement.vehicles.models import Vehicle

        self.UserRole = UserRole
        self.Driver = Driver
        self.Vehicle = Vehicle
        self.EmergencyIncident = EmergencyIncident
        self.EmergencyType = EmergencyType
        self.EmergencyStatus = EmergencyStatus

        # Create roles in an idempotent way to avoid UNIQUE collisions
        self.driver_role, _ = self.UserRole.objects.get_or_create(
            name=self.UserRole.DRIVER if hasattr(self.UserRole, 'DRIVER') else 'DRIVER',
            defaults={'description': ''}
        )
        self.admin_role, _ = self.UserRole.objects.get_or_create(
            name=self.UserRole.ADMIN if hasattr(self.UserRole, 'ADMIN') else 'ADMIN',
            defaults={'description': ''}
        )

        # Create users
        from conftest import TEST_PASSWORD
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password=TEST_PASSWORD,
            role=self.admin_role
        )

        self.driver_user = User.objects.create_user(
            username='driver_user',
            email='driver@example.com',
            password=TEST_PASSWORD,
            role=self.driver_role
        )

        # Create vehicle
        import uuid
        self.vehicle = self.Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2022,
            license_plate=f'ABC-{uuid.uuid4().hex[:6].upper()}',
            vin=f'1HGCM82633A{uuid.uuid4().hex[:6].upper()}'
        )

        # Provide license_expiry_date for backward compatibility with DB schema
        self.driver = self.Driver.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='123-456-7890',
            driver_license_number=f'DL{timezone.now().timestamp():.0f}',
            license_expiry_date=timezone.now().date(),
            hire_date=timezone.now().date(),
        )
        # Create emergency incident
        self.incident = self.EmergencyIncident.objects.create(
            vehicle=self.vehicle,
            driver=self.driver,
            reported_by=self.admin_user,
            emergency_type=self.EmergencyType.ACCIDENT,
            status=self.EmergencyStatus.REPORTED,
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
        self.assertEqual(self.incident.emergency_type, self.EmergencyType.ACCIDENT)
        self.assertEqual(self.incident.status, self.EmergencyStatus.REPORTED)
        self.assertEqual(self.incident.location, 'Highway 101, Mile Marker 25')
        self.assertEqual(self.incident.latitude, Decimal('37.7749'))
        self.assertEqual(self.incident.longitude, Decimal('-122.4194'))
        self.assertEqual(self.incident.description, 'Vehicle involved in a minor collision.')
        self.assertIsNotNone(self.incident.reported_time)
        self.assertIsNone(self.incident.resolved_time)

    def test_incident_string_representation(self):
        """Test EmergencyIncident string representation."""
        expected_str = f"Accident - Toyota Camry ({self.vehicle.license_plate}) - {self.incident.reported_time.strftime('%Y-%m-%d %H:%M')}"
        self.assertEqual(str(self.incident), expected_str)

    def test_incident_status_update(self):
        """Test updating EmergencyIncident status."""
        # Update to responding
        self.incident.status = self.EmergencyStatus.RESPONDING
        self.incident.save()
        self.assertEqual(self.incident.status, self.EmergencyStatus.RESPONDING)

        # Update to resolved
        self.incident.status = self.EmergencyStatus.RESOLVED
        self.incident.resolved_time = timezone.now()
        self.incident.save()
        self.assertEqual(self.incident.status, self.EmergencyStatus.RESOLVED)
        self.assertIsNotNone(self.incident.resolved_time)

        # Update to closed
        self.incident.status = self.EmergencyStatus.CLOSED
        self.incident.save()
        self.assertEqual(self.incident.status, self.EmergencyStatus.CLOSED)

class EmergencyResponseTestCase(APITestCase):
    """Test cases for the EmergencyResponse model."""

    def setUp(self):
        """Set up test environment."""
        from CarFleetManagement.accounts.models import Driver, UserRole
        from CarFleetManagement.emergency.models import (
            EmergencyIncident,
            EmergencyResponse,
            EmergencyStatus,
            EmergencyType,
        )
        from CarFleetManagement.vehicles.models import Vehicle

        self.UserRole = UserRole
        self.Driver = Driver
        self.Vehicle = Vehicle
        self.EmergencyIncident = EmergencyIncident
        self.EmergencyType = EmergencyType
        self.EmergencyStatus = EmergencyStatus
        self.EmergencyResponse = EmergencyResponse

        # Create roles in an idempotent way to avoid UNIQUE collisions when
        # tests run in different orders
        self.driver_role, _ = self.UserRole.objects.get_or_create(
            name=self.UserRole.DRIVER if hasattr(self.UserRole, 'DRIVER') else 'DRIVER',
            defaults={'description': ''}
        )
        self.admin_role, _ = self.UserRole.objects.get_or_create(
            name=self.UserRole.ADMIN if hasattr(self.UserRole, 'ADMIN') else 'ADMIN',
            defaults={'description': ''}
        )

        # Create users
        from conftest import TEST_PASSWORD
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password=TEST_PASSWORD,
            role=self.admin_role
        )
        self.responder_user = User.objects.create_user(
            username='responder_user',
            email='responder@example.com',
            password=TEST_PASSWORD,
            role=self.admin_role
        )
        # Create driver
        from django.utils import timezone
        self.driver = self.Driver.objects.create(
            first_name='Test',
            last_name='DriverUser',
            driver_license_number=f'D{int(timezone.now().timestamp())}',
            license_expiry_date=timezone.now().date(),
            hire_date=timezone.now().date()
        )

        # Create vehicle
        import uuid
        self.vehicle = self.Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2022,
            license_plate=f'ABC-{uuid.uuid4().hex[:6].upper()}',
            vin=f'1HGCM82633A{uuid.uuid4().hex[:6].upper()}'
        )

        # Create emergency incident
        self.incident = self.EmergencyIncident.objects.create(
            vehicle=self.vehicle,
            driver=self.driver,
            reported_by=self.admin_user,
            emergency_type=self.EmergencyType.BREAKDOWN,
            status=self.EmergencyStatus.REPORTED,
            location='Highway 101, Mile Marker 25',
            description='Vehicle engine failure.'
        )

        # Create emergency response
        self.response = self.EmergencyResponse.objects.create(
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
        expected_str = f"Response to {self.response.incident} by {self.response.responder.username}"
        self.assertEqual(str(self.response), expected_str)

class EmergencyContactTestCase(APITestCase):
    """Test cases for the EmergencyContact model in the emergency app."""

    def setUp(self):
        """Set up test environment."""
        from CarFleetManagement.emergency.models import EmergencyContact
        self.EmergencyContact = EmergencyContact

        from conftest import TEST_PASSWORD
        self.user = User.objects.create_user(
            username='test_user',
            email='user@example.com',
            password=TEST_PASSWORD
        )

        self.emergency_contact = self.EmergencyContact.objects.create(
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
        expected_str = "Jane Doe (Spouse) - 123-456-7890"
        self.assertEqual(str(self.emergency_contact), expected_str)
