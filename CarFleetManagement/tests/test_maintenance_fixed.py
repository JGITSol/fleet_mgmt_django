from datetime import timedelta

import pytest
from django.utils import timezone

from CarFleetManagement.maintenance.models import Maintenance
from CarFleetManagement.vehicles.models import Vehicle


@pytest.mark.django_db
def test_maintenance_simple():
    """A very simple test to verify maintenance functionality."""
    # Create a test vehicle
    vehicle = Vehicle.objects.create(
        brand='TestBrand',
        model='TestModel',
        year=2022,
        license_plate='TEST-123',
        vin='TEST12345678901234',
        status='AVAILABLE'
    )

    # Create a maintenance record
    future_date = timezone.now().date() + timedelta(days=5)
    maintenance = Maintenance.objects.create(
        vehicle=vehicle,
        maintenance_type='ROUTINE',
        status='SCHEDULED',
        description='Test maintenance',
        scheduled_date=future_date,
        odometer_reading=10000,
        cost=100.00,
        service_provider='Test Provider'
    )

    # Basic assertions
    assert maintenance.vehicle == vehicle
    assert maintenance.maintenance_type == 'ROUTINE'
    assert maintenance.status == 'SCHEDULED'

    # Test days_until_scheduled
    days = maintenance.days_until_scheduled()
    assert isinstance(days, int)
    assert days > 0
