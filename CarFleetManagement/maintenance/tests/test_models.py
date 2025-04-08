from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from maintenance.models import Maintenance, MaintenanceType, MaintenanceStatus
from vehicles.models import Vehicle

class MaintenanceTestCase(TestCase):
    """Test cases for the Maintenance model."""
    
    def setUp(self):
        """Set up test environment."""
        self.today = timezone.now().date()
        
        # Create a test vehicle
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
        
        self.inspection_maintenance = Maintenance.objects.create(
            vehicle=self.vehicle,
            maintenance_type=MaintenanceType.INSPECTION,
            status=MaintenanceStatus.COMPLETED,
            description='Annual vehicle inspection',
            scheduled_date=self.today - timedelta(days=5),
            completed_date=self.today - timedelta(days=5),
            odometer_reading=16000,
            cost=Decimal('75.00'),
            service_provider='State Inspection Center',
            notes='Passed inspection'
        )
    
    def test_maintenance_creation(self):
        """Test Maintenance creation."""
        self.assertEqual(self.routine_maintenance.vehicle, self.vehicle)
        self.assertEqual(self.routine_maintenance.maintenance_type, MaintenanceType.ROUTINE)
        self.assertEqual(self.routine_maintenance.status, MaintenanceStatus.SCHEDULED)
        self.assertEqual(self.routine_maintenance.description, 'Regular oil change and inspection')
        self.assertEqual(self.routine_maintenance.scheduled_date, self.today + timedelta(days=7))
        self.assertEqual(self.routine_maintenance.odometer_reading, 15000)
        self.assertEqual(self.routine_maintenance.cost, Decimal('150.00'))
        self.assertEqual(self.routine_maintenance.service_provider, 'AutoCare Service Center')
        self.assertEqual(self.routine_maintenance.notes, 'Reminder to check brake pads')
    
    def test_maintenance_string_representation(self):
        """Test Maintenance string representation."""
        expected_str = f"Routine Maintenance for Toyota Camry (ABC-123) on {(self.today + timedelta(days=7)).strftime('%Y-%m-%d')}"
        self.assertEqual(str(self.routine_maintenance), expected_str)
    
    def test_maintenance_type_choices(self):
        """Test Maintenance type choices."""
        self.assertEqual(self.routine_maintenance.maintenance_type, MaintenanceType.ROUTINE)
        self.assertEqual(self.repair_maintenance.maintenance_type, MaintenanceType.REPAIR)
        self.assertEqual(self.inspection_maintenance.maintenance_type, MaintenanceType.INSPECTION)
        
        # Test changing maintenance type
        self.routine_maintenance.maintenance_type = MaintenanceType.OTHER
        self.routine_maintenance.save()
        self.assertEqual(self.routine_maintenance.maintenance_type, MaintenanceType.OTHER)
    
    def test_maintenance_status_choices(self):
        """Test Maintenance status choices."""
        self.assertEqual(self.routine_maintenance.status, MaintenanceStatus.SCHEDULED)
        self.assertEqual(self.repair_maintenance.status, MaintenanceStatus.IN_PROGRESS)
        self.assertEqual(self.inspection_maintenance.status, MaintenanceStatus.COMPLETED)
        
        # Test changing maintenance status
        self.routine_maintenance.status = MaintenanceStatus.CANCELLED
        self.routine_maintenance.save()
        self.assertEqual(self.routine_maintenance.status, MaintenanceStatus.CANCELLED)
    
    def test_days_until_scheduled(self):
        """Test days_until_scheduled method."""
        # For scheduled maintenance
        days_until = self.routine_maintenance.days_until_scheduled()
        self.assertEqual(days_until, 7)
        
        # For in-progress maintenance
        days_until = self.repair_maintenance.days_until_scheduled()
        self.assertEqual(days_until, 0)
        
        # For completed maintenance
        days_until = self.inspection_maintenance.days_until_scheduled()
        self.assertIsNone(days_until)
        
        # For cancelled maintenance
        self.routine_maintenance.status = MaintenanceStatus.CANCELLED
        self.routine_maintenance.save()
        days_until = self.routine_maintenance.days_until_scheduled()
        self.assertIsNone(days_until)