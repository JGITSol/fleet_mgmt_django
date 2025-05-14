from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from rest_framework_simplejwt.tokens import RefreshToken

from maintenance.models import Maintenance, MaintenanceType, MaintenanceStatus
from vehicles.models import Vehicle
from accounts.models import UserRole

User = get_user_model()

# ========================
# Appended from project-level tests/test_maintenance.py
# ========================
import pytest
from django.utils import timezone
from datetime import timedelta

from maintenance.models import Maintenance
from vehicles.models import Vehicle

@pytest.mark.django_db
def test_maintenance_creation():
    """Test maintenance record creation."""
    # Create test vehicle
    vehicle = Vehicle.objects.create(
        brand='Test Brand',
        model='Test Model',
        year=2022,
        license_plate='TEST123',
        vin='TEST12345678901234',
        status='AVAILABLE'
    )
    
    # Create test maintenance
    maintenance = Maintenance.objects.create(
        vehicle=vehicle,
        maintenance_type='ROUTINE',
        status='COMPLETED',
        description='Test maintenance',
        scheduled_date=timezone.now().date(),
        completed_date=timezone.now().date(),
        odometer_reading=10000,
        cost=50.00,
        service_provider='Test Provider',
        notes='Test notes'
    )
    
    # Verify the maintenance was created
    assert maintenance.id is not None
    assert maintenance.vehicle == vehicle
    assert maintenance.maintenance_type == 'ROUTINE'
    assert maintenance.cost == 50.00

class MaintenanceViewsTestCase(APITestCase):
    """Test cases for the maintenance app views."""
    
    def setUp(self):
        """Set up test environment."""
        # Create roles
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN, description='Administrator role')
        self.maintenance_role = UserRole.objects.create(name=UserRole.MAINTENANCE_STAFF, description='Maintenance Staff role')
        
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=self.admin_role
        )
        
        self.maintenance_user = User.objects.create_user(
            username='maintenance_user',
            email='maintenance@example.com',
            password='password123',
            role=self.maintenance_role
        )
        
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
        
        # Create client

        self.token = RefreshToken.for_user(self.maintenance_user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_maintenance_list_view(self):
        """Test maintenance list view."""
        # Test maintenance list view
        response = self.client.get(reverse('maintenance:maintenance_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Regular oil change and inspection')
        self.assertContains(response, 'Replace faulty alternator')
    
    def test_maintenance_detail_view(self):
        """Test maintenance detail view."""
        # Test maintenance detail view
        response = self.client.get(reverse('maintenance:maintenance_detail', kwargs={'pk': self.routine_maintenance.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Regular oil change and inspection')
        self.assertContains(response, 'AutoCare Service Center')
    
    def test_maintenance_create_view(self):
        """Test maintenance create view."""
        # Test GET request
        response = self.client.get(reverse('maintenance:maintenance_create'))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
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
        
        response = self.client.post(reverse('maintenance:maintenance_create'), maintenance_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Verify maintenance record was created
        self.assertTrue(Maintenance.objects.filter(description='Annual vehicle inspection').exists())
    
    def test_maintenance_update_view(self):
        """Test maintenance update view."""
        # Test GET request
        response = self.client.get(reverse('maintenance:maintenance_update', kwargs={'pk': self.repair_maintenance.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request - mark maintenance as completed
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
        
        response = self.client.post(reverse('maintenance:maintenance_update', kwargs={'pk': self.repair_maintenance.pk}), updated_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Verify maintenance record was updated
        self.repair_maintenance.refresh_from_db()
        self.assertEqual(self.repair_maintenance.status, MaintenanceStatus.COMPLETED)
        self.assertEqual(self.repair_maintenance.notes, 'Repair completed successfully')