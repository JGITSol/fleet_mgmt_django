from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from maintenance.models import Maintenance, MaintenanceType, MaintenanceStatus
from maintenance.serializers import MaintenanceSerializer
from vehicles.models import Vehicle
from accounts.models import UserRole, CustomUser

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework_simplejwt.tokens import RefreshToken

class MaintenanceAPITestCase(APITestCase):
    def setUp(self):
        """Set up test environment."""
        # Create roles
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN, description='Administrator role')
        self.maintenance_role = UserRole.objects.create(name=UserRole.MAINTENANCE_STAFF, description='Maintenance Staff role')
        
        # Create users
        self.admin_user = CustomUser.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=self.admin_role
        )
        
        self.maintenance_user = CustomUser.objects.create_user(
            username='maintenance_user',
            email='maintenance@example.com',
            password='password123',
            role=self.maintenance_role
        )
        
        # Generate JWT tokens
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.maintenance_token = str(RefreshToken.for_user(self.maintenance_user).access_token)
        
        # Create vehicle
        self.today = timezone.now().date()
        self.vehicle = Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2022,
            license_plate='ABC-123',
            vin='1HGCM82633A123456'
        )
        
        # Create maintenance records
        self.routine_maintenance = Maintenance.objects.create(
            vehicle=self.vehicle,
            maintenance_type=MaintenanceType.ROUTINE,
            status=MaintenanceStatus.SCHEDULED,
            description='Regular oil change and inspection',
            scheduled_date=self.today + timedelta(days=7),
            odometer_reading=15000,
            cost=Decimal('150.00'),
            service_provider='AutoCare Service Center',
            notes='Reminder to check brake pads'
        )
        
        self.repair_maintenance = Maintenance.objects.create(
            vehicle=self.vehicle,
            maintenance_type=MaintenanceType.REPAIR,
            status=MaintenanceStatus.IN_PROGRESS,
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
        # Authenticate as admin
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        # Make API request
        response = self.client.get(reverse('CarFleetManagement.api:api-maintenance-list'))
        
        # Get data from DB
        maintenance_records = Maintenance.objects.all()
        serializer = MaintenanceSerializer(maintenance_records, many=True)
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_get_single_maintenance(self):
        """Test retrieving a single maintenance record."""
        # Authenticate as maintenance staff
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.maintenance_token}')
        
        # Make API request
        response = self.client.get(reverse('CarFleetManagement.api:api-maintenance-detail', kwargs={'pk': self.routine_maintenance.pk}))
        
        # Get data from DB
        maintenance = Maintenance.objects.get(pk=self.routine_maintenance.pk)
        serializer = MaintenanceSerializer(maintenance)
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_maintenance(self):
        """Test creating a new maintenance record."""
        # Authenticate as maintenance staff
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.maintenance_token}')
        
        # Prepare data
        maintenance_data = {
            'vehicle': self.vehicle.id,
            'maintenance_type': MaintenanceType.INSPECTION,
            'status': MaintenanceStatus.SCHEDULED,
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
        self.assertEqual(Maintenance.objects.count(), 3)
        self.assertTrue(Maintenance.objects.filter(description='Annual vehicle inspection').exists())
    
    def test_update_maintenance(self):
        """Test updating a maintenance record."""
        # Authenticate as maintenance staff
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.maintenance_token}')
        
        # Prepare data - mark maintenance as completed
        updated_data = {
            'vehicle': self.vehicle.id,
            'maintenance_type': MaintenanceType.REPAIR,
            'status': MaintenanceStatus.COMPLETED,  # Changed from IN_PROGRESS to COMPLETED
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
        self.assertEqual(self.repair_maintenance.status, MaintenanceStatus.COMPLETED)
        self.assertEqual(self.repair_maintenance.notes, 'Repair completed successfully')
    
    def test_delete_maintenance(self):
        """Test deleting a maintenance record."""
        # Authenticate as admin
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        # Make API request
        response = self.client.delete(reverse('CarFleetManagement.api:api-maintenance-detail', kwargs={'pk': self.routine_maintenance.pk}))
        
        # Assert response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Maintenance.objects.count(), 1)
        self.assertFalse(Maintenance.objects.filter(pk=self.routine_maintenance.pk).exists())
    
    def test_unauthorized_access(self):
        """Test unauthorized access to maintenance API."""
        # Unauthenticated request
        self.client.credentials()  # Clear credentials
        response = self.client.get(reverse('CarFleetManagement.api:api-maintenance-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Create a regular user without maintenance permissions
        regular_user = CustomUser.objects.create_user(
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