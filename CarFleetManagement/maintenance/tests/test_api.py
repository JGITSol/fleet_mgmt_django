from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

# Vehicle model import moved into setUp method
# UserRole and CustomUser model imports moved into setUp method
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

# Model imports moved into setUp method
from CarFleetManagement.maintenance.serializers import MaintenanceSerializer

User = get_user_model()

from tests.auth_utils import AuthTestMixin  # Import AuthTestMixin


class MaintenanceAPITestCase(APITestCase, AuthTestMixin): # Inherit from AuthTestMixin
    def setUp(self):
        """Set up test environment."""
        from CarFleetManagement.accounts.models import CustomUser, UserRole
        from CarFleetManagement.maintenance.models import (
            Maintenance,
            MaintenanceStatus,
            MaintenanceType,
        )
        from CarFleetManagement.vehicles.models import Vehicle
        self.Maintenance = Maintenance
        self.MaintenanceType = MaintenanceType
        self.MaintenanceStatus = MaintenanceStatus
        self.Vehicle = Vehicle
        self.UserRole = UserRole
        self.CustomUser = CustomUser

        # Create roles
        self.admin_role = self.UserRole.objects.create(name=self.UserRole.ADMIN, description='Administrator role')
        self.maintenance_role = self.UserRole.objects.create(name=self.UserRole.MAINTENANCE_STAFF, description='Maintenance Staff role')

        # Create users
        self.admin_user = self.CustomUser.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=self.admin_role
        )

        # Create users
        self.maintenance_user = self.CustomUser.objects.create_user(
            username='maintenance_user',
            email='maintenance@example.com',
            password='password123',
            role=self.maintenance_role
        )

        # Generate JWT tokens for potential use if specific tests need to switch users
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.maintenance_token = str(RefreshToken.for_user(self.maintenance_user).access_token)

        # Initialize client and authenticate as admin_user by default
        # self.client, _ = self.get_authenticated_client(self.admin_user) # Moved to individual tests

        # Create vehicle
        self.today = timezone.now().date()
        self.vehicle = self.Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2022,
            license_plate='ABC-123',
            vin='1HGCM82633A123456'
        )

        # Create maintenance records
        self.routine_maintenance = self.Maintenance.objects.create(
            vehicle=self.vehicle,
            maintenance_type=self.MaintenanceType.ROUTINE,
            status=self.MaintenanceStatus.SCHEDULED,
            description='Regular oil change and inspection',
            scheduled_date=self.today + timedelta(days=7),
            odometer_reading=15000,
            cost=Decimal('150.00'),
            service_provider='AutoCare Service Center',
            notes='Reminder to check brake pads'
        )

        self.repair_maintenance = self.Maintenance.objects.create(
            vehicle=self.vehicle,
            maintenance_type=self.MaintenanceType.REPAIR,
            status=self.MaintenanceStatus.IN_PROGRESS,
            description='Replace faulty alternator',
            scheduled_date=self.today,
            completed_date=None,
            odometer_reading=16500,
            cost=Decimal('450.00'),
            service_provider='AutoCare Service Center',
            notes='Parts on order'
        )

        # Create API client


    def test_get_all_maintenance(self):
        """Test retrieving all maintenance records."""
        self.client, _ = self.get_authenticated_client(self.admin_user)
        # client is already authenticated as admin_user from setUp

        # Make API request
        response = self.client.get(reverse('CarFleetManagement.api:api-maintenance-list'))

        # Get data from DB
        maintenance_records = self.Maintenance.objects.all()
        serializer = MaintenanceSerializer(maintenance_records, many=True)

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_maintenance(self):
        """Test retrieving a single maintenance record."""
        self.client, _ = self.get_authenticated_client(self.admin_user)
        # client is already authenticated as admin_user from setUp
        # If this test specifically needs maintenance_user, re-authenticate or create a new client:
        # temp_client, _ = self.get_authenticated_client(self.maintenance_user)
        # response = temp_client.get(...)

        # Make API request
        response = self.client.get(reverse('CarFleetManagement.api:api-maintenance-detail', kwargs={'pk': self.routine_maintenance.pk}))

        # Get data from DB
        maintenance = self.Maintenance.objects.get(pk=self.routine_maintenance.pk)
        serializer = MaintenanceSerializer(maintenance)

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_maintenance(self):
        """Test creating a new maintenance record."""
        self.client, _ = self.get_authenticated_client(self.admin_user)
        # client is already authenticated as admin_user from setUp
        # If this test specifically needs maintenance_user for creation, adjust accordingly.

        # Prepare data
        maintenance_data = {
            'vehicle': self.vehicle.id,
            'maintenance_type': self.MaintenanceType.INSPECTION,
            'status': self.MaintenanceStatus.SCHEDULED,
            'description': 'Annual vehicle inspection',
            'scheduled_date': self.today + timedelta(days=14),
            'odometer_reading': 17000,
            'cost': '75.00',
            'service_provider': 'Vehicle Inspection Center',
            'notes': 'Required for registration renewal'
        }

        # Make API request
        response = self.client.post(reverse('CarFleetManagement.api:api-maintenance-list'), maintenance_data, format='json')

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.Maintenance.objects.count(), 3)
        self.assertTrue(self.Maintenance.objects.filter(description='Annual vehicle inspection').exists())

    def test_update_maintenance(self):
        """Test updating an existing maintenance record."""
        self.client, _ = self.get_authenticated_client(self.admin_user)
        # client is already authenticated as admin_user from setUp

        # Prepare data - mark maintenance as completed
        updated_data = {
            'vehicle': self.vehicle.id,
            'maintenance_type': self.MaintenanceType.REPAIR,
            'status': self.MaintenanceStatus.COMPLETED,  # Changed from IN_PROGRESS to COMPLETED
            'description': 'Replace faulty alternator',
            'scheduled_date': self.today,
            'completed_date': self.today,  # Added completion date
            'odometer_reading': 16500,
            'cost': '450.00',
            'service_provider': 'AutoCare Service Center',
            'notes': 'Repair completed successfully'
        }

        # Make API request
        response = self.client.put(
            reverse('CarFleetManagement.api:api-maintenance-detail', kwargs={'pk': self.repair_maintenance.pk}),
            updated_data,
            format='json'
        )

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify maintenance record was updated
        self.repair_maintenance.refresh_from_db()
        self.assertEqual(self.repair_maintenance.status, self.MaintenanceStatus.COMPLETED)
        self.assertEqual(self.repair_maintenance.notes, 'Repair completed successfully')

    def test_delete_maintenance(self):
        """Test deleting a maintenance record."""
        self.client, _ = self.get_authenticated_client(self.admin_user)
        # client is already authenticated as admin_user from setUp

        # Make API request
        response = self.client.delete(reverse('CarFleetManagement.api:api-maintenance-detail', kwargs={'pk': self.routine_maintenance.pk}))

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.Maintenance.objects.count(), 1)
        self.assertFalse(self.Maintenance.objects.filter(pk=self.routine_maintenance.pk).exists())

    def test_unauthorized_access_maintenance(self):
        """Test unauthorized access to maintenance API."""
        # Unauthenticated request
        unauthenticated_client = APIClient() # Create a new unauthenticated client
        response = unauthenticated_client.get(reverse('CarFleetManagement.api:api-maintenance-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Create a regular user without maintenance permissions
        regular_user = self.CustomUser.objects.create_user(
            username='regular_user',
            email='regular@example.com',
            password='password123'
        )

        # Authenticate as regular user
        from rest_framework_simplejwt.tokens import RefreshToken
        regular_token = str(RefreshToken.for_user(regular_user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {regular_token}')

        # Try to delete a maintenance record
        response = self.client.delete(reverse('CarFleetManagement.api:api-maintenance-detail', kwargs={'pk': self.routine_maintenance.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
