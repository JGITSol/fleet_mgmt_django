from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.test import APITestCase


class MaintenanceTestCase(APITestCase):
    """Test cases for the Maintenance model."""

    def setUp(self):
        """Set up test environment."""
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

        self.today = timezone.now().date()

        # Create a test vehicle
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

        self.inspection_maintenance = self.Maintenance.objects.create(
            vehicle=self.vehicle,
            maintenance_type=self.MaintenanceType.INSPECTION,
            status=self.MaintenanceStatus.COMPLETED,
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
        self.assertEqual(self.routine_maintenance.maintenance_type, self.MaintenanceType.ROUTINE)
        self.assertEqual(self.routine_maintenance.status, self.MaintenanceStatus.SCHEDULED)
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
        self.assertEqual(self.routine_maintenance.maintenance_type, self.MaintenanceType.ROUTINE)
        self.assertEqual(self.repair_maintenance.maintenance_type, self.MaintenanceType.REPAIR)
        self.assertEqual(self.inspection_maintenance.maintenance_type, self.MaintenanceType.INSPECTION)

        # Test changing maintenance type
        self.routine_maintenance.maintenance_type = self.MaintenanceType.OTHER
        self.routine_maintenance.save()
        self.assertEqual(self.routine_maintenance.maintenance_type, self.MaintenanceType.OTHER)

    def test_maintenance_status_choices(self):
        """Test Maintenance status choices."""
        self.assertEqual(self.routine_maintenance.status, self.MaintenanceStatus.SCHEDULED)
        self.assertEqual(self.repair_maintenance.status, self.MaintenanceStatus.IN_PROGRESS)
        self.assertEqual(self.inspection_maintenance.status, self.MaintenanceStatus.COMPLETED)

        # Test changing maintenance status
        self.routine_maintenance.status = self.MaintenanceStatus.CANCELLED
        self.routine_maintenance.save()
        self.assertEqual(self.routine_maintenance.status, self.MaintenanceStatus.CANCELLED)

    def test_days_until_scheduled(self):
        """Test days_until_scheduled method."""
        # For scheduled maintenance
        days_until = self.routine_maintenance.days_until_scheduled()
        expected_days = (self.routine_maintenance.scheduled_date - self.today).days
        self.assertEqual(days_until, expected_days)

        # For in-progress maintenance
        days_until = self.repair_maintenance.days_until_scheduled()
        expected_days = (self.repair_maintenance.scheduled_date - self.today).days
        self.assertEqual(days_until, expected_days)

        # For completed maintenance
        days_until = self.inspection_maintenance.days_until_scheduled()
        self.assertIsNone(days_until)

        # For cancelled maintenance
        self.routine_maintenance.status = self.MaintenanceStatus.CANCELLED
        self.routine_maintenance.save()
        days_until = self.routine_maintenance.days_until_scheduled()
        self.assertIsNone(days_until)

    def test_negative_odometer_not_allowed(self):
        """Test negative odometer reading is not allowed."""

        maintenance = self.Maintenance(
            vehicle=self.vehicle,
            maintenance_type=self.MaintenanceType.ROUTINE,
            status=self.MaintenanceStatus.SCHEDULED,
            description='Negative odometer',
            scheduled_date=self.today + timedelta(days=1),
            odometer_reading=-100,
            cost=10,
            service_provider='Test',
            notes=''
        )
        with self.assertRaises(ValidationError):
            maintenance.full_clean()

    def test_missing_scheduled_date(self):
        """Test days_until_scheduled returns 0 if scheduled_date is None."""
        maintenance = self.Maintenance(
            vehicle=self.vehicle,
            maintenance_type=self.MaintenanceType.ROUTINE,
            status=self.MaintenanceStatus.SCHEDULED,
            description='No date',
            scheduled_date=None,
            odometer_reading=1000,
            cost=10,
            service_provider='Test',
            notes=''
        )
        self.assertEqual(maintenance.days_until_scheduled(), 0)

    def test_invalid_status(self):
        """Test invalid status raises error."""
        from django.core.exceptions import ValidationError
        maintenance = self.Maintenance(
            vehicle=self.vehicle,
            maintenance_type=self.MaintenanceType.ROUTINE,
            status='INVALID',
            description='Bad status',
            scheduled_date=self.today,
            odometer_reading=1000,
            cost=10,
            service_provider='Test',
            notes=''
        )
        with self.assertRaises(ValidationError):
            maintenance.full_clean()

    def test_str_for_all_types(self):
        """Test __str__ for all maintenance types."""
        for mtype in self.MaintenanceType:
            self.routine_maintenance.maintenance_type = mtype
            self.routine_maintenance.save()
            self.assertIn(str(mtype.label), str(self.routine_maintenance))

    def test_cost_validation(self):
        """Test negative cost is not allowed."""
        from django.core.exceptions import ValidationError
        maintenance = self.Maintenance(
            vehicle=self.vehicle,
            maintenance_type=self.MaintenanceType.ROUTINE,
            status=self.MaintenanceStatus.SCHEDULED,
            description='Negative cost',
            scheduled_date=self.today + timedelta(days=1),
            odometer_reading=1000,
            cost=-10,
            service_provider='Test',
            notes=''
        )
        with self.assertRaises(ValidationError):
            maintenance.full_clean()
