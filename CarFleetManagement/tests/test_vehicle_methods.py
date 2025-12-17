from datetime import timedelta

import pytest
from django.utils import timezone

from CarFleetManagement.vehicles.models import Vehicle


@pytest.mark.django_db
class TestVehicleMethods:
    """Test Vehicle model methods."""

    def create_vehicle(self, **kwargs):
        import uuid
        defaults = {
            'brand': 'Toyota',
            'model': 'Camry',
            'year': 2022,
            'license_plate': f'ABC-{uuid.uuid4().hex[:6].upper()}',
            'vin': f'1HGCM82633A{uuid.uuid4().hex[:6].upper()}',
            'status': 'AVAILABLE'
        }
        defaults.update(kwargs)
        return Vehicle.objects.create(**defaults)

    def test_is_service_due_with_future_date(self):
        """Test is_service_due method with a future date."""
        # Create a vehicle with next service date in the future
        today = timezone.now().date()
        future_date = today + timedelta(days=30)

        vehicle = self.create_vehicle(next_service_date=future_date)

        # Service should not be due
        assert not vehicle.is_service_due()

    def test_is_service_due_with_past_date(self):
        """Test is_service_due method with a past date."""
        # Create a vehicle with next service date in the past
        today = timezone.now().date()
        past_date = today - timedelta(days=30)

        vehicle = self.create_vehicle(next_service_date=past_date)

        # Service should be due
        assert vehicle.is_service_due()

    def test_is_service_due_with_today(self):
        """Test is_service_due method with today's date."""
        # Create a vehicle with next service date as today
        today = timezone.now().date()

        vehicle = self.create_vehicle(next_service_date=today)

        # Service should be due
        assert vehicle.is_service_due()

    def test_is_service_due_with_no_date(self):
        """Test is_service_due method with no service date."""
        # Create a vehicle with no next service date
        vehicle = self.create_vehicle(next_service_date=None)

        # Service should not be due if no date is set
        assert not vehicle.is_service_due()

    def test_update_mileage(self):
        """Test updating vehicle mileage."""
        # Create a vehicle
        vehicle = self.create_vehicle(mileage=10000)

        # Update mileage
        vehicle.mileage = 15000
        vehicle.save()

        # Verify mileage was updated
        updated_vehicle = Vehicle.objects.get(id=vehicle.id)
        assert updated_vehicle.mileage == 15000

    def test_vehicle_status_update(self):
        """Test updating vehicle status."""
        # Create a vehicle
        vehicle = self.create_vehicle()

        # Update status
        vehicle.status = 'MAINTENANCE'
        vehicle.save()

        # Verify status was updated
        updated_vehicle = Vehicle.objects.get(id=vehicle.id)
        assert updated_vehicle.status == 'MAINTENANCE'
